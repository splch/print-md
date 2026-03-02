-- mermaid.lua — Render Mermaid diagrams to PNG via mmdc (mermaid-cli)
--
-- Finds code blocks with class "mermaid", renders them via mmdc,
-- and replaces them with Image elements pointing to the generated PNG.
-- If mmdc is not available, code blocks pass through unchanged.

local mmdc_available = nil  -- nil = not yet checked

local function check_mmdc()
  if mmdc_available ~= nil then
    return mmdc_available
  end
  local handle = io.popen("mmdc --version 2>/dev/null")
  if handle then
    local result = handle:read("*a")
    handle:close()
    if result and result:match("%S") then
      mmdc_available = true
      return true
    end
  end
  mmdc_available = false
  return false
end

local diagram_count = 0

function CodeBlock(el)
  if not el.classes:includes("mermaid") then
    return nil
  end

  if not check_mmdc() then
    io.stderr:write("[print_md] mmdc not found, rendering mermaid block as code\n")
    return nil
  end

  diagram_count = diagram_count + 1

  -- Create temp files for mmdc input/output
  local tmp_base = os.tmpname()
  local input_file = tmp_base .. ".mmd"
  local output_file = tmp_base .. ".png"

  -- Write mermaid source to temp file
  local f = io.open(input_file, "w")
  if not f then
    io.stderr:write("[print_md] warning: could not create temp file for mermaid diagram\n")
    return nil
  end
  f:write(el.text)
  f:close()

  -- Run mmdc to render PNG
  local cmd = string.format(
    'mmdc -i "%s" -o "%s" -b transparent --quiet -s 4 2>&1',
    input_file, output_file
  )
  local handle = io.popen(cmd)
  local result = handle:read("*a")
  handle:close()

  -- Clean up input file immediately
  os.remove(input_file)
  os.remove(tmp_base)

  -- Check if PNG was created
  local png_check = io.open(output_file, "r")
  if not png_check then
    io.stderr:write(string.format(
      "[print_md] warning: mermaid diagram %d failed to render: %s\n",
      diagram_count, result or "unknown error"
    ))
    return nil
  end
  png_check:close()

  -- Build caption from optional attribute
  local caption_text = el.attributes["caption"] or ""
  local caption = pandoc.Inlines({})
  if caption_text ~= "" then
    caption = pandoc.Inlines(caption_text)
  end

  -- Create Image element pointing to the PNG file
  local img = pandoc.Image(caption, output_file)

  return pandoc.Para({img})
end
