declare module "node:fs" { const value: any; export default value; }
declare module "node:path" { const value: any; export default value; }
declare module "node:url" { export function fileURLToPath(value: string | URL): string; }
declare module "node:assert/strict" { const value: any; export default value; }
declare module "node:test" { const value: any; export default value; }
declare const process: { version: string; exitCode?: number };
