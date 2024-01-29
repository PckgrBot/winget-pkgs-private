import { VercelRequest, VercelResponse } from "@vercel/node";
import { createKysely } from "@vercel/postgres-kysely";

export default async function handler(req: VercelRequest, res: VercelResponse) {
  // only allow POST requests
  if (req.method !== "POST") {
    res.status(405).send("Method Not Allowed");
    return;
  }

  // Parse the request body as JSON
  const { Query, Inclusions, Filters, MaxiumumResults } = req.body as {
    Query: SearchRequestMatch;
    Inclusions: SearchRequestInclusionAndFilterSchema;
    Filters: SearchRequestInclusionAndFilterSchema;
    MaxiumumResults: number;
  };
  console.log(`Query: ${JSON.stringify(Query, null, 0)}`);
  console.log(`Inclusions: ${JSON.stringify(Inclusions, null, 0)}`);
  console.log(`Filters: ${JSON.stringify(Filters, null, 0)}`);
  console.log(`MaxiumumResults: ${MaxiumumResults}`);

  let [hostHead] = process.env.PGHOST!.split(".");
  const db = createKysely<Database>({
    connectionString: process.env.DATABASE_URL!.replace(
      hostHead,
      `${hostHead}-pooler`
    ),
  });
  let query = db.selectFrom("packages").selectAll();

  if (Query) {
    if (Query.MatchType === "Exact") {
      query = query.where("PackageIdentifier", "=", Query.KeyWord);
    } else if (Query.MatchType === "CaseInsensitive") {
      query = query.where("PackageIdentifier", "ilike", Query.KeyWord);
    } else if (Query.MatchType === "StartsWith") {
      query = query.where("PackageIdentifier", "ilike", `${Query.KeyWord}%`);
    } else {
      query = query.where("PackageIdentifier", "ilike", `%${Query.KeyWord}%`);
    }
  }

  // combine both Inclusions and Filters into a single array
  let inclusionsAndFilters: SearchRequestInclusionAndFilterSchema = [];
  if (Inclusions) {
    inclusionsAndFilters = inclusionsAndFilters.concat(Inclusions);
  }
  if (Filters) {
    inclusionsAndFilters = inclusionsAndFilters.concat(Filters);
  }

  // apply each inclusion and filter to the query
  if (inclusionsAndFilters.length > 0) {
    //@ts-ignore
    query = query.where((eb) => {
      const ors: any = [];

      for (const inclusionOrFilter of inclusionsAndFilters) {
        switch (inclusionOrFilter.PackageMatchField) {
          case "NormalizedPackageNameAndPublisher":
            ors.push(
              eb(
                "PackageName",
                "ilike",
                `%${inclusionOrFilter.RequestMatch.KeyWord}%`
              )
            );
            ors.push(
              eb(
                "Publisher",
                "ilike",
                `%${inclusionOrFilter.RequestMatch.KeyWord}%`
              )
            );
            break;
          case "Command":
          case "Tag":
            ors.push(
              eb(
                eb.val(inclusionOrFilter.RequestMatch.KeyWord),
                "ilike",
                // Table names are "Commands"/"Tags", not "Command"/"Tag"
                eb.fn.any(`${inclusionOrFilter.PackageMatchField}s`)
              )
            );
            break;
          case "PackageFamilyName":
          case "ProductCode":
            ors.push(
              eb(
                eb.val(inclusionOrFilter.RequestMatch.KeyWord),
                "ilike",
                eb.fn.any(inclusionOrFilter.PackageMatchField)
              )
            );
            break;
          case "Market":
            // we do not support filtering by market
            break;
          default:
            ors.push(
              eb(
                inclusionOrFilter.PackageMatchField,
                `${
                  inclusionOrFilter.RequestMatch.MatchType === "Exact"
                    ? "="
                    : "ilike"
                }`,
                `${
                  ["Exact", "CaseInsensitive"].includes(
                    inclusionOrFilter.RequestMatch.MatchType
                  )
                    ? inclusionOrFilter.RequestMatch.KeyWord
                    : inclusionOrFilter.RequestMatch.MatchType === "StartsWith"
                    ? `${inclusionOrFilter.RequestMatch.KeyWord}%`
                    : `%${inclusionOrFilter.RequestMatch.KeyWord}%`
                }`
              )
            );
            break;
        }

        return eb.or(ors);
      }
    });
  }

  if (MaxiumumResults) {
    query = query.limit(MaxiumumResults);
  }

  // execute the query and return the results
  console.log(`SQL: ${query.compile().sql}`);
  console.log(`Params: ${JSON.stringify(query.compile().parameters, null, 0)}`);
  const results = await query.execute();

  if (!results || results.length === 0) {
    return res.status(204).end();
  }

  let data: {}[] = [];
  for (const result of results) {
    data.push({
      PackageIdentifier: result.PackageIdentifier,
      PackageName: result.PackageName,
      Publisher: result.Publisher,
      Versions: [
        {
          PackageVersion: result.PackageVersion,
          // note: it is "PackageFamilyNames" not "PackageFamilyName
          PackageFamilyNames: result.PackageFamilyName,
          // note: it is "ProductCodes" not "ProductCode"
          ProductCodes: result.ProductCode,
        },
      ],
    });
  }

  res.status(200).json({
    Data: data,
    UnsupportedPackageMatchFields: ["Market"],
  });
}

interface Database {
  packages: PackagesTable;
}

interface PackagesTable {
  PackageIdentifier: string;
  PackageVersion: string;
  PackageName: string;
  Publisher: string;
  Moniker: string;
  ProductCode: string[];
  Commands: string[];
  Tags: string[];
  PackageFamilyName: string[];
}

type SearchRequestInclusionAndFilterSchema = Array<{
  PackageMatchField:
    | "PackageIdentifier"
    | "PackageName"
    | "Moniker"
    | "Command"
    | "Tag"
    | "PackageFamilyName"
    | "ProductCode"
    | "NormalizedPackageNameAndPublisher"
    | "Market";
  RequestMatch: SearchRequestMatch;
}>;

type SearchRequestMatch = {
  KeyWord: string;
  MatchType:
    | "Exact"
    | "CaseInsensitive"
    | "StartsWith"
    | "Substring"
    | "Wildcard"
    | "Fuzzy"
    | "FuzzySubstring";
};
