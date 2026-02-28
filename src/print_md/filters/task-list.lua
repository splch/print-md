-- task-list.lua — Render GFM task list checkboxes for Typst output
--
-- Converts [ ] and [x] in bullet lists into Typst checkbox symbols.

function Div(el)
  -- Pandoc wraps task list items in a Div with class "task-list"
  -- We don't need to modify the Div itself
  return el
end

function Plain(el)
  if #el.content == 0 then
    return el
  end

  local first = el.content[1]

  -- Check for unchecked box: ☐
  if first.tag == "Str" and first.text == "☐" then
    el.content[1] = pandoc.RawInline("typst", "#box(stroke: 0.5pt + luma(120), width: 0.55em, height: 0.55em, radius: 1.5pt, inset: 0pt)")
    return el
  end

  -- Check for checked box: ☒
  if first.tag == "Str" and first.text == "☒" then
    el.content[1] = pandoc.RawInline("typst", "#box(stroke: 0.5pt + luma(120), width: 0.55em, height: 0.55em, radius: 1.5pt, inset: 0pt, fill: luma(80))[#align(center + horizon)[#text(fill: white, size: 0.45em)[✓]]]")
    return el
  end

  return el
end
