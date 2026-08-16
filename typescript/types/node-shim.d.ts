declare module "node:fs" { const value: any; export default value; }
declare module "node:path" { const value: any; export default value; }
declare module "node:url" { export function fileURLToPath(value: string | URL): string; }
declare module "node:assert/strict" { const value: any; export default value; }
declare module "node:test" { const value: any; export default value; }
declare module "node:http" { const value: any; export default value; }
declare module "node:events" { export function once(...args: any[]): Promise<any[]>; }
declare module "node:crypto" {
  export function createHash(algorithm: string): { update(value: string): any; digest(encoding: string): string };
  export function randomUUID(): string;
}
declare const Buffer: { concat(chunks: any[]): { toString(encoding: string): string } };
declare const process: { version: string; exitCode?: number; argv: string[]; env: Record<string, string | undefined> };
