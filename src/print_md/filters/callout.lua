-- callout.lua — Convert fenced divs (.note, .tip) to styled Typst callout blocks.
-- Pandoc's Typst writer drops div classes, so this filter wraps the content
-- in raw Typst function calls that the template can style.

function Div(el)
  local class = nil
  if el.classes:includes("note") then
    class = "callout-note"
  elseif el.classes:includes("tip") then
    class = "callout-tip"
  end
  if class then
    local open = pandoc.RawBlock("typst", "#" .. class .. "[")
    local close = pandoc.RawBlock("typst", "]")
    local blocks = pandoc.List({open})
    blocks:extend(el.content)
    blocks:insert(close)
    return blocks
  end
end
