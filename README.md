# osrs-wiki-maps
A set of tools for generating map images for the OSRS wiki.

## Generating maps
1. Add the latest cache in idx format to `./data/cache`
2. Add xteas in a format that RuneLite's `XteaManager` can process into `./data/xteas.json`.
3. Run `MapExport.java`
4. Run `scripts/stitch.py`.
