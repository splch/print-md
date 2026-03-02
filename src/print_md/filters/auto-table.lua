-- auto-table.lua — Use auto-sized table columns for Typst output.
--
-- Pandoc's Typst writer emits fixed-width columns (equal fractions or
-- percentages), which causes ugly wrapping when content lengths vary.
-- This filter re-renders each table with `columns: (auto, auto, ...)`
-- so Typst sizes columns to fit their content.

function Table(el)
  local ncols = #el.colspecs
  local doc = pandoc.Pandoc({el})
  local typst = pandoc.write(doc, "typst")
  local autos = {}
  for i = 1, ncols do autos[i] = "auto" end
  local auto_str = "columns: (" .. table.concat(autos, ",") .. "),"
  -- Replace `columns: N,` (equal-width) or `columns: (...),` (percentage-based)
  typst = typst:gsub("columns: %d+,", auto_str)
  typst = typst:gsub("columns: %b(),", auto_str)
  return pandoc.RawBlock("typst", typst)
end
