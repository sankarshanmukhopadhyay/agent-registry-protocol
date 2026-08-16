import fs from "node:fs";
import path from "node:path";
import { repositoryRoot } from "./repository.js";

export interface SchemaDescriptor {
  file: string;
  id: string;
  draft: string;
  title?: string;
}

function walk(dir: string): string[] {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry: any) => {
    const full = path.join(dir, entry.name);
    return entry.isDirectory() ? walk(full) : entry.name.endsWith(".schema.json") ? [full] : [];
  });
}

/** Load the normative JSON Schema catalog without maintaining a TypeScript copy of protocol definitions. */
export function loadSchemaCatalog(): SchemaDescriptor[] {
  return walk(path.join(repositoryRoot, "schemas")).sort().map((file) => {
    const schema = JSON.parse(fs.readFileSync(file, "utf8")) as Record<string, unknown>;
    const id = schema.$id;
    const draft = schema.$schema;
    if (typeof id !== "string" || typeof draft !== "string") {
      throw new Error(`Schema lacks $id or $schema: ${file}`);
    }
    return {
      file: path.relative(repositoryRoot, file),
      id,
      draft,
      ...(typeof schema.title === "string" ? { title: schema.title } : {})
    };
  });
}
