-- florilegium-theme-rooms.lua: a florilegium theme for the dark-rooms worksheet. It has no
-- plant. The margin holds mirror rooms cut from the 45-degree lattice tiling, with light rays:
--   - behind everything, a faint ray that bounces down the margin column from corner to corner,
--     and one or two large pale pieces of the tiling;
--   - on each page, one famous dark room from literature, with its title and author;
--   - on pages where a part begins, Peyton's 22-wall room in the bottom corner, its three
--     copies of the staircase in three tones, and the ray from S toward T that stops at a corner;
--   - beside each numbered section heading, a copper A star;
--   - along the bottom, a corridor with a ray that bounces between its walls into a corner;
--   - everywhere else, largest hole first: small rooms with a ray traced until it hits a corner,
--     unfolded mirror copies, A stars, patches of the tiling, cell shapes with their outside
--     neighbors, and A, B, and C points.
-- Use: \usepackage[grown,theme=rooms]{florilegium}, with this file beside the document.
-- The theme doesn't support florilegium's growth animation.

local ink = require("florilegium-ink")
local M = {}

local floor, min, max, abs, sqrt = math.floor, math.min, math.max, math.abs, math.sqrt
local tone = ink.tone
local WHITE = { 1, 1, 1 }
local W_WALL, W_THIN, W_RAY = 0.75, 0.25, 0.55        -- line widths in bp

-- ---------------------------------------------------------------- lattice pieces, in lattice units
local function key(x, y) return x .. "," .. y end
local function square(x, y, a, b) ink.poly({ { x, y }, { x + a, y }, { x + a, y + b }, { x, y + b } }, true) end

-- a lattice point by parity: A (even, even) filled, B (odd, odd) open, C (mixed) a small square
local function mark(x, y, r, c)
  local ex, ey = x % 2 == 0, y % 2 == 0
  if ex and ey then ink.circle(x, y, r) ink.fill(c)
  elseif not ex and not ey then
    ink.circle(x, y, r) ink.fill(WHITE)
    ink.circle(x, y, r) ink.stroke(c, 0.3)
  else square(x - 0.8 * r, y - 0.8 * r, 1.6 * r, 1.6 * r) ink.fill(c) end
end

-- the tiling's diagonal in the unit square at (x, y): from its even-even corner to its odd-odd one
local function diagonal(x, y)
  if (x + y) % 2 == 0 then ink.moveto(x, y) ink.lineto(x + 1, y + 1)
  else ink.moveto(x + 1, y) ink.lineto(x, y + 1) end
end

local function bbox(cells)
  local x0, y0, x1, y1 = math.huge, math.huge, -math.huge, -math.huge
  for _, c in ipairs(cells) do
    x0, y0, x1, y1 = min(x0, c[1]), min(y0, c[2]), max(x1, c[1] + 1), max(y1, c[2] + 1)
  end
  return x0, y0, x1, y1
end

local function set_of(cells)
  local s = {}
  for _, c in ipairs(cells) do s[key(c[1], c[2])] = true end
  return s
end

-- the boundary of a hole-free, pinch-free set of unit cells, counterclockwise, corners only
local function outline(cells, set)
  local nxt, first = {}, nil
  local function edge(ax, ay, bx, by) nxt[key(ax, ay)] = { bx, by } first = first or { ax, ay } end
  for _, c in ipairs(cells) do
    local x, y = c[1], c[2]
    if not set[key(x, y - 1)] then edge(x, y, x + 1, y) end
    if not set[key(x + 1, y)] then edge(x + 1, y, x + 1, y + 1) end
    if not set[key(x, y + 1)] then edge(x + 1, y + 1, x, y + 1) end
    if not set[key(x - 1, y)] then edge(x, y + 1, x, y) end
  end
  local pts, p = {}, first
  repeat pts[#pts + 1] = p p = nxt[key(p[1], p[2])] until p[1] == first[1] and p[2] == first[2]
  local out = {}
  for i, q in ipairs(pts) do
    local a, b = pts[(i - 2) % #pts + 1], pts[i % #pts + 1]
    if (q[1] - a[1]) * (b[2] - q[2]) ~= (q[2] - a[2]) * (b[1] - q[1]) then out[#out + 1] = q end
  end
  return out
end

-- true when the cells form a room: no two cells meet only at a corner, and no hole
local function simple(cells, set)
  for _, c in ipairs(cells) do
    for _, d in ipairs({ { 1, 1 }, { 1, -1 } }) do
      if set[key(c[1] + d[1], c[2] + d[2])] and not set[key(c[1] + d[1], c[2])] and not set[key(c[1], c[2] + d[2])] then
        return false
      end
    end
  end
  local x0, y0, x1, y1 = bbox(cells)
  x0, y0, x1, y1 = x0 - 1, y0 - 1, x1, y1
  local seen, stack, n = { [key(x0, y0)] = true }, { { x0, y0 } }, 1
  while #stack > 0 do
    local p = table.remove(stack)
    for _, d in ipairs({ { 1, 0 }, { -1, 0 }, { 0, 1 }, { 0, -1 } }) do
      local x, y = p[1] + d[1], p[2] + d[2]
      local k = key(x, y)
      if x >= x0 and x <= x1 and y >= y0 and y <= y1 and not set[k] and not seen[k] then
        seen[k] = true n = n + 1 stack[#stack + 1] = { x, y }
      end
    end
  end
  return n == (x1 - x0 + 1) * (y1 - y0 + 1) - #cells
end

-- n connected unit cells grown at random, retried until they form a room
local function polyomino(rng, n)
  for _ = 1, 30 do
    local cells, set = { { 0, 0 } }, { ["0,0"] = true }
    while #cells < n do
      local c = cells[rng.int(1, #cells)]
      local d = ({ { 1, 0 }, { -1, 0 }, { 0, 1 }, { 0, -1 } })[rng.int(1, 4)]
      local x, y = c[1] + d[1], c[2] + d[2]
      if not set[key(x, y)] then set[key(x, y)] = true cells[#cells + 1] = { x, y } end
    end
    if simple(cells, set) then return cells, set end
  end
  return { { 0, 0 }, { 1, 0 } }, set_of({ { 0, 0 }, { 1, 0 } })
end

-- a light path in a room of unit cells, from p in direction d (both parts nonzero). It bounces
-- off walls, passes lattice points inside the room or on a straight wall, and stops at a corner.
-- Returns the points and whether it stopped at a corner; after `bounces` bounces it ends a
-- little past the last one.
local function trace(set, p, d, bounces)
  local x, y, dx, dy = p[1], p[2], d[1], d[2]
  local pts, n = { { x, y } }, 0
  local function at(cx, cy) return set[key(cx, cy)] end
  for _ = 1, 200 do
    local cx, cy = floor(x + dx * 1e-6), floor(y + dy * 1e-6)
    local sx, sy = dx > 0 and 1 or -1, dy > 0 and 1 or -1
    local nx, ny = dx > 0 and cx + 1 or cx, dy > 0 and cy + 1 or cy
    local tx, ty = (nx - x) / dx, (ny - y) / dy
    local t = min(tx, ty)
    if n >= bounces then
      pts[#pts + 1] = { x + dx * t * 0.7, y + dy * t * 0.7 }
      return pts, false
    end
    local hx, hy = abs(tx - t) < 1e-9, abs(ty - t) < 1e-9
    x, y = hx and nx or x + dx * t, hy and ny or y + dy * t
    local X, Y = at(cx + sx, cy), at(cx, cy + sy)
    if hx and hy then
      local D = at(cx + sx, cy + sy)
      if X and Y and D then
      elseif X and not Y and not D then dy = -dy n = n + 1 pts[#pts + 1] = { x, y }
      elseif Y and not X and not D then dx = -dx n = n + 1 pts[#pts + 1] = { x, y }
      else pts[#pts + 1] = { x, y } return pts, true end
    elseif hx and not X then dx = -dx n = n + 1 pts[#pts + 1] = { x, y }
    elseif hy and not Y then dy = -dy n = n + 1 pts[#pts + 1] = { x, y } end
  end
  pts[#pts + 1] = { x, y }
  return pts, false
end

-- the ray: a copper line from a dark dot, ending in a cross at a corner or an arrowhead.
-- u is the size of a lattice unit in cm, so the dots and heads keep their size on the page.
local function ray(pts, stopped, u, dashed)
  local c = ink.accent(0)
  ink.layer(5)
  ink.poly(pts)
  ink.stroke(c, W_RAY, 1, false, dashed and "[1.6 1.2] 0" or nil)
  local a, b = pts[#pts - 1], pts[#pts]
  local s = 0.07 / u
  if stopped then
    ink.moveto(b[1] - s, b[2] - s) ink.lineto(b[1] + s, b[2] + s)
    ink.moveto(b[1] - s, b[2] + s) ink.lineto(b[1] + s, b[2] - s)
    ink.stroke(c, W_RAY * 1.3)
  else
    local dx, dy = b[1] - a[1], b[2] - a[2]
    local L = sqrt(dx * dx + dy * dy)
    dx, dy = dx / L, dy / L
    local h = 0.13 / u
    ink.poly({ { b[1] + dx * h * 0.3, b[2] + dy * h * 0.3 }, { b[1] - dx * h - dy * h * 0.4, b[2] - dy * h + dx * h * 0.4 },
      { b[1] - dx * h + dy * h * 0.4, b[2] - dy * h - dx * h * 0.4 } }, true)
    ink.fill(c)
  end
  ink.circle(pts[1][1], pts[1][2], 0.045 / u) ink.fill(tone(0.08))
  ink.layer(3)
end

-- a room: its cells (each may carry its own tone), the tiling inside, and the walls
local function draw_room(cells, set, fill, u)
  ink.layer(2)
  for _, c in ipairs(cells) do square(c[1] - 0.01, c[2] - 0.01, 1.02, 1.02) ink.fill(c.tone and tone(c.tone) or fill) end
  ink.layer(3)
  for _, c in ipairs(cells) do diagonal(c[1], c[2]) end
  ink.stroke(tone(0.62), W_THIN)
  ink.poly(outline(cells, set), true)
  ink.stroke(tone(0.22), W_WALL)
end

-- ---------------------------------------------------------------- the motifs, centered at (0, 0) within radius R (cm)
local DIRS = { { 1, 2 }, { 2, 1 }, { 1, 3 }, { 3, 1 }, { 2, 3 }, { 3, 2 }, { 1, 1 } }

local function small_room(layout, R)
  local n = layout.int(R > 0.9 and 5 or 3, R > 0.9 and 11 or 6)
  local cells, set = polyomino(layout, n)
  local x0, y0, x1, y1 = bbox(cells)
  local u = 2 * R / (max(x1 - x0, y1 - y0) + 0.5)
  local c = cells[layout.int(1, #cells)]
  local d = DIRS[layout.int(1, #DIRS)]
  d = { layout.chance(0.5) and d[1] or -d[1], layout.chance(0.5) and d[2] or -d[2] }
  local pts, stopped = trace(set, { c[1] + 0.5, c[2] + 0.5 }, d, layout.int(2, 5))
  local fill = tone(layout.range(0.9, 0.95))
  local turn = layout.chance(0.35) and 45 or 0
  if turn ~= 0 then u = u / 1.3 end
  return function()
    ink.push() ink.rotate(turn) ink.scale(u) ink.translate(-(x0 + x1) / 2, -(y0 + y1) / 2)
    draw_room(cells, set, fill, u)
    ray(pts, stopped, u)
    ink.pop()
  end
end

-- an A star: the eight tiles around an A point, in two alternating tones, with its B and C points
local function star(layout, R, accent)
  local t1, t2 = layout.range(0.5, 0.68), layout.range(0.8, 0.9)
  local turn = layout.chance(0.3) and 45 or 0
  return function()
    local function body()
      ink.push() ink.rotate(turn) ink.scale(R / 1.45)
      local P = { { 1, 0 }, { 1, 1 }, { 0, 1 }, { -1, 1 }, { -1, 0 }, { -1, -1 }, { 0, -1 }, { 1, -1 } }
      for k = 1, 8 do
        ink.poly({ { 0, 0 }, P[k], P[k % 8 + 1] }, true)
        ink.fill(tone(k % 2 == 0 and t1 or t2))
      end
      for k = 1, 8, 2 do ink.moveto(0, 0) ink.lineto(P[k + 1][1], P[k + 1][2]) end
      square(-1, -1, 2, 2)
      ink.stroke(tone(0.2), W_THIN * 1.6)
      local r = 0.05 / (R / 1.45)
      for _, p in ipairs(P) do mark(p[1], p[2], r, tone(0.1)) end
      mark(0, 0, r * 1.3, tone(0.05))
      ink.pop()
    end
    if accent then ink.in_accent(body) else body() end
  end
end

-- a patch of the tiling, with every lattice point marked
local function tiles(layout, R)
  local w, h = layout.int(2, 4), layout.int(2, 3)
  local ox, oy = layout.int(0, 1), layout.int(0, 1)
  local u = 2 * R / (max(w, h) + 0.3)
  return function()
    ink.push() ink.scale(u) ink.translate(-ox - w / 2, -oy - h / 2)
    for x = ox, ox + w do ink.moveto(x, oy) ink.lineto(x, oy + h) end
    for y = oy, oy + h do ink.moveto(ox, y) ink.lineto(ox + w, y) end
    for x = ox, ox + w - 1 do for y = oy, oy + h - 1 do diagonal(x, y) end end
    ink.stroke(tone(0.45), W_THIN * 1.4)
    for x = ox, ox + w do for y = oy, oy + h do mark(x, y, 0.045 / u, tone(0.12)) end end
    ink.pop()
  end
end

-- full cells (dark) and their outside neighbors (copper dots), as in the four-cell bound
local SHAPES = {
  { { 0, 0 }, { 1, 0 }, { 2, 0 }, { 3, 0 } }, { { 0, 0 }, { 1, 0 }, { 0, 1 }, { 1, 1 } },
  { { 0, 0 }, { 1, 0 }, { 2, 0 }, { 1, 1 } }, { { 0, 0 }, { 1, 0 }, { 1, 1 }, { 2, 1 } },
  { { 0, 0 }, { 0, 1 }, { 0, 2 }, { 1, 0 } }, { { 0, 0 }, { 1, 0 }, { 0, 1 } }, { { 0, 0 }, { 1, 1 } },
}
local function cells(layout, R)
  local shape = SHAPES[layout.int(1, #SHAPES)]
  local set = set_of(shape)
  local x0, y0, x1, y1 = bbox(shape)
  x0, y0, x1, y1 = x0 - 1, y0 - 1, x1 + 1, y1 + 1
  local u = 2 * R / (max(x1 - x0, y1 - y0) + 0.2)
  local dark = layout.range(0.25, 0.4)
  return function()
    ink.push() ink.scale(u) ink.translate(-(x0 + x1) / 2, -(y0 + y1) / 2)
    for _, c in ipairs(shape) do square(c[1], c[2], 1, 1) ink.fill(tone(dark)) end
    for x = x0, x1 do ink.moveto(x, y0) ink.lineto(x, y1) end
    for y = y0, y1 do ink.moveto(x0, y) ink.lineto(x1, y) end
    ink.stroke(tone(0.6), W_THIN)
    local seen = {}
    for _, c in ipairs(shape) do
      for _, d in ipairs({ { 1, 0 }, { -1, 0 }, { 0, 1 }, { 0, -1 } }) do
        local x, y = c[1] + d[1], c[2] + d[2]
        if not set[key(x, y)] and not seen[key(x, y)] then
          seen[key(x, y)] = true
          ink.circle(x + 0.5, y + 0.5, 0.055 / u) ink.fill(ink.accent(0))
        end
      end
    end
    ink.pop()
  end
end

-- unfolding: a rectangle and its mirror copies, the straight segment from S to an image of T
-- (dashed), and the real path it folds back to (solid)
local function unfold(layout, R)
  local w, h = layout.int(2, 3), layout.int(1, 2)
  local a, b = layout.int(2, 3), layout.int(1, 2)
  if a * w < 3 then a = 3 end
  local s = { layout.int(1, 2 * w - 1) / 2, layout.int(1, 2 * h - 1) / 2 }
  local t = { layout.int(1, 2 * w - 1) / 2, layout.int(1, 2 * h - 1) / 2 }
  local function img(i, j)
    return i % 2 == 0 and i * w + t[1] or (i + 1) * w - t[1], j % 2 == 0 and j * h + t[2] or (j + 1) * h - t[2]
  end
  local tx, ty = img(a - 1, b - 1)
  -- the crossings of the segment with the copies' edges, in order, then folded into the room
  local ts = {}
  for k = 1, a - 1 do ts[#ts + 1] = (k * w - s[1]) / (tx - s[1]) end
  if ty ~= s[2] then for k = 1, b - 1 do ts[#ts + 1] = (k * h - s[2]) / (ty - s[2]) end end
  table.sort(ts)
  local function fold(v, L) v = v % (2 * L) return v > L and 2 * L - v or v end
  local real = { { s[1], s[2] } }
  for _, k in ipairs(ts) do
    if k > 0 and k < 1 then real[#real + 1] = { fold(s[1] + k * (tx - s[1]), w), fold(s[2] + k * (ty - s[2]), h) } end
  end
  real[#real + 1] = { t[1], t[2] }
  local u = 2 * R / (max(a * w, b * h) + 0.4)
  return function()
    ink.push() ink.scale(u) ink.translate(-a * w / 2, -b * h / 2)
    ink.layer(2) square(0, 0, w, h) ink.fill(tone(0.92))
    ink.layer(3)
    for i = 0, a - 1 do for j = 0, b - 1 do
      if i + j > 0 then square(i * w, j * h, w, h) ink.stroke(tone(0.55), W_THIN * 1.6, 1, false, "[1.2 1] 0") end
    end end
    square(0, 0, w, h) ink.stroke(tone(0.12), W_WALL)
    ray({ { s[1], s[2] }, { tx, ty } }, false, u, true)
    ink.layer(5) ink.poly(real) ink.stroke(ink.accent(0), W_RAY) ink.layer(3)
    ink.circle(t[1], t[2], 0.045 / u) ink.fill(tone(0.08))
    ink.circle(tx, ty, 0.045 / u) ink.fill(WHITE)
    ink.circle(tx, ty, 0.045 / u) ink.stroke(ink.accent(0), 0.4)
    ink.pop()
  end
end

-- Peyton's room: the staircase P and its copies P1 (reflected) and P2 (turned), with the ray
-- from S = (0, 0) toward T = (2, 2) that stops at the corner (1, 1)
local P0 = { { -1, -1 }, { 0, -1 }, { 0, -2 }, { 1, -2 }, { 1, -3 } }
local function room22(R)
  local cl, tones = {}, { 0.9, 0.8, 0.85 }
  for _, c in ipairs(P0) do
    cl[#cl + 1] = { c[1], c[2], tone = tones[1] }
    cl[#cl + 1] = { c[1], -c[2] - 1, tone = tones[2] }
    cl[#cl + 1] = { 3 - c[1], -c[2] - 1, tone = tones[3] }
  end
  local set = set_of(cl)
  local u = 2 * R / 6.3
  return function()
    ink.push() ink.scale(u) ink.translate(-2, 0)
    draw_room(cl, set, nil, u)
    ink.moveto(-1, 0) ink.lineto(1, 0) ink.moveto(2, 1) ink.lineto(2, 3)
    ink.stroke(tone(0.3), W_THIN * 2, 1, false, "[1.5 1.2] 0")
    for _, p in ipairs({ { -1, 0 }, { 1, 0 }, { 2, 1 }, { 2, 3 } }) do mark(p[1], p[2], 0.05 / u, ink.accent(0)) end
    ray({ { 0, 0 }, { 1, 1 } }, true, u)
    ink.circle(2, 2, 0.045 / u) ink.fill(tone(0.08))
    ink.pop()
  end
end

-- the corridor along the bottom: one unit high, closed at both ends, the tiling inside; the
-- ray leaves (0.5, 0.5), bounces at lattice points on the long walls, and stops at a far corner
local function corridor(x0, y0, x1, h)
  local L = floor((x1 - x0) / h)
  if L < 3 then return end
  local pts = { { 0.5, 0.5 }, { 1, 1 } }
  for k = 2, L do pts[#pts + 1] = { k, k % 2 } end
  ink.push() ink.translate(x0, y0) ink.scale(h)
  local cl = {}
  for k = 0, L - 1 do cl[#cl + 1] = { k, 0 } end
  draw_room(cl, set_of(cl), tone(0.94), h)
  ray(pts, true, h)
  ink.pop()
end

-- ---------------------------------------------------------------- famous dark rooms from literature
-- Each is drawn in its own units inside `box`; draw(s) gets the size of one unit in cm.

-- c mixed toward white by v, then made as pale as the rest of the margin
local function wash(c, v)
  local p = ink.set_pale(0) ink.set_pale(p)
  local k = 1 - (1 - v) * (1 - p)
  return { c[1] + (1 - c[1]) * k, c[2] + (1 - c[2]) * k, c[3] + (1 - c[3]) * k }
end

local function ngon(n, R, a0, cx, cy)
  local p = {}
  for k = 0, n - 1 do
    local a = math.rad(a0 + 360 * k / n)
    p[#p + 1] = { (cx or 0) + R * math.cos(a), (cy or 0) + R * math.sin(a) }
  end
  return p
end

local function arc(cx, cy, r, a0, a1, n)
  local p = {}
  for k = 0, n do local a = math.rad(a0 + (a1 - a0) * k / n) p[#p + 1] = { cx + r * math.cos(a), cy + r * math.sin(a) } end
  return p
end

local function seg(a, b, c, d) ink.moveto(a, b) ink.lineto(c, d) end

-- p reflected across the line through a and b
local function reflect(p, a, b)
  local ex, ey = b[1] - a[1], b[2] - a[2]
  local t = ((p[1] - a[1]) * ex + (p[2] - a[2]) * ey) / (ex * ex + ey * ey)
  local fx, fy = a[1] + t * ex, a[2] + t * ey
  return { 2 * fx - p[1], 2 * fy - p[2] }
end

-- a light path in a convex polygon from p in direction d: n bounces, then part of the next leg
local function bounce(poly, p, d, n)
  local pts, x, y, dx, dy = { { p[1], p[2] } }, p[1], p[2], d[1], d[2]
  for k = 0, n do
    local best, nx, ny = math.huge, 0, 0
    for i = 1, #poly do
      local a, b = poly[i], poly[i % #poly + 1]
      local ex, ey = b[1] - a[1], b[2] - a[2]
      local den = dx * ey - dy * ex
      if abs(den) > 1e-12 then
        local t = ((a[1] - x) * ey - (a[2] - y) * ex) / den
        local s = ((a[1] - x) * dy - (a[2] - y) * dx) / den
        if t > 1e-9 and s >= 0 and s <= 1 and t < best then
          local L = sqrt(ex * ex + ey * ey)
          best, nx, ny = t, -ey / L, ex / L
        end
      end
    end
    if k == n then pts[#pts + 1] = { x + dx * best * 0.55, y + dy * best * 0.55 } break end
    x, y = x + dx * best, y + dy * best
    local q = 2 * (dx * nx + dy * ny)
    dx, dy = dx - q * nx, dy - q * ny
    pts[#pts + 1] = { x, y }
  end
  return pts
end

local WALL = 0.22                                  -- the tone of a wall

-- Poe: seven chambers, each a sharp turn from the last, the seventh black with scarlet panes
local MASQUE = { { 0.15, 0.3, 0.8 }, { 0.5, 0.15, 0.6 }, { 0.15, 0.6, 0.3 }, { 0.95, 0.5, 0.1 },
  { 1, 1, 1 }, { 0.55, 0.3, 0.9 }, { 0.05, 0.05, 0.08 } }
local function masque(s)
  local cl = {}
  for k = 0, 6 do cl[#cl + 1] = { floor((k + 1) / 2), -floor(k / 2) } end
  ink.push() ink.rotate(-45) ink.translate(-2, 1)
  ink.layer(2)
  for k, c in ipairs(cl) do square(c[1], c[2], 1, 1) ink.fill(wash(MASQUE[k], k == 7 and 0 or 0.5)) end
  ink.layer(3)
  for k = 1, 6 do                                    -- inner walls, each with a doorway
    local a, b = cl[k], cl[k + 1]
    if b[1] > a[1] then seg(b[1], b[2], b[1], b[2] + 0.3) seg(b[1], b[2] + 0.7, b[1], b[2] + 1)
    else seg(a[1], a[2], a[1] + 0.3, a[2]) seg(a[1] + 0.7, a[2], a[1] + 1, a[2]) end
  end
  ink.stroke(tone(WALL), W_THIN * 2)
  ink.poly(outline(cl, set_of(cl)), true) ink.stroke(tone(WALL), W_WALL)
  seg(3.25, -3, 3.75, -3) ink.stroke(wash({ 0.8, 0.05, 0.05 }, 0), 2.2)
  local walk = {}
  for _, c in ipairs(cl) do walk[#walk + 1] = { c[1] + 0.5, c[2] + 0.5 } end
  ray(walk, false, s, true)
  ink.pop()
end

-- Leroux: the hexagonal torture chamber lined with mirrors, with its iron tree. The six
-- dashed rooms are the tree's first reflections.
local TREE = { { 0.3, -0.5, 0.3, 0.05 }, { 0.3, -0.15, 0.05, 0.12 }, { 0.3, -0.25, 0.55, 0.0 },
  { 0.3, 0.05, 0.4, 0.3 }, { 0.3, 0.05, 0.15, 0.32 } }
local function phantom(s)
  local hex = ngon(6, 1, 0)
  local function tree(f)
    for _, t in ipairs(TREE) do
      local a, b = f({ t[1], t[2] }), f({ t[3], t[4] })
      seg(a[1], a[2], b[1], b[2])
    end
  end
  for i = 1, 6 do
    local a, b = hex[i], hex[i % 6 + 1]
    local img = {}
    for k, p in ipairs(hex) do img[k] = reflect(p, a, b) end
    ink.poly(img, true) ink.stroke(tone(0.6), W_THIN * 1.6, 1, false, "[1.2 1] 0")
    tree(function(p) return reflect(p, a, b) end) ink.stroke(tone(0.62), 0.6)
  end
  ink.layer(2) ink.poly(hex, true) ink.fill(tone(0.88)) ink.layer(3)
  ink.poly(ngon(6, 0.94, 0), true) ink.stroke(tone(0.55), W_THIN * 1.4)
  ink.poly(hex, true) ink.stroke(tone(WALL), W_WALL * 1.3)
  tree(function(p) return p end) ink.stroke(tone(0.15), 0.9)
  ray(bounce(hex, { -0.55, -0.35 }, { math.cos(math.rad(14)), math.sin(math.rad(14)) }, 6), false, s)
end

-- Borges: hexagonal galleries joined by narrow vestibules. Four walls hold shelves, a railed
-- shaft drops through the middle, two lamps light each one, and a spiral stair and a
-- mirror stand in the vestibule.
local function babel(s)
  local H = 0.866
  local cy = { 1.066, -1.066 }
  ink.layer(2)
  for _, y in ipairs(cy) do ink.poly(ngon(6, 1, 0, 0, y), true) ink.fill(tone(0.9)) end
  for _, y in ipairs({ -2.25, -0.2, 1.932 }) do square(-0.25, y, 0.5, 0.32 + (y == -0.2 and 0.08 or 0)) ink.fill(tone(0.9)) end
  ink.layer(3)
  for _, y in ipairs(cy) do
    local h = ngon(6, 1, 0, 0, y)
    for _, i in ipairs({ 1, 3, 4, 6 }) do                   -- the four walls of shelves
      local a, b = h[i], h[i % 6 + 1]
      seg(a[1], a[2], b[1], b[2])
      local mx, my = (a[1] + b[1]) / 2, (a[2] + b[2]) / 2
      local ix, iy = -mx * 0.13, -(my - y) * 0.13
      seg(a[1] + ix, a[2] + iy, b[1] + ix, b[2] + iy)
      for k = 1, 4 do
        local t = k / 5
        local px, py = a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t
        seg(px, py, px + ix, py + iy)
      end
    end
    for _, sy in ipairs({ 1, -1 }) do                       -- the two walls that open to vestibules
      seg(-0.5, y + sy * H, -0.25, y + sy * H) seg(0.25, y + sy * H, 0.5, y + sy * H)
    end
    ink.stroke(tone(WALL), W_WALL)
    ink.poly(ngon(6, 0.3, 0, 0, y), true) ink.fill(tone(0.55))
    ink.poly(ngon(6, 0.36, 0, 0, y), true) ink.stroke(tone(0.35), W_THIN * 1.6)
    for _, lx in ipairs({ -0.55, 0.55 }) do ink.circle(lx, y, 0.06) ink.fill(ink.accent(0)) end
  end
  for _, y0 in ipairs({ -2.25, -0.2, 1.932 }) do
    local y1 = y0 + (y0 == -0.2 and 0.4 or 0.32)
    seg(-0.25, y0, -0.25, y1) seg(0.25, y0, 0.25, y1)
  end
  ink.stroke(tone(WALL), W_WALL)
  seg(-0.24, -0.15, -0.24, 0.15) ink.stroke(tone(0.45), 1.4)        -- the mirror
  local sp = {}
  for k = 0, 40 do local a = k * 0.45 sp[#sp + 1] = { 0.06 + 0.012 * a * math.cos(a), 0.012 * a * math.sin(a) } end
  ink.poly(sp) ink.stroke(tone(0.3), W_THIN * 1.6)                  -- the spiral stair
end

-- Plato: prisoners chained to face the back wall; a fire behind a low wall throws the
-- shadows of carried things onto it. Daylight is up the passage.
local function cave(s)
  local F = { 0.85, -0.25 }
  local inside = { { -1.4, -0.7 }, { 1.05, -0.7 }, { 1.5, 0.1 }, { 1.5, 0.75 }, { 1.1, 0.75 }, { 0.6, 0.45 }, { -1.4, 0.45 } }
  ink.layer(2) ink.poly(inside, true) ink.fill(tone(0.84)) ink.layer(3)
  ink.poly({ { 1.1, 0.75 }, { 0.6, 0.45 }, { -1.4, 0.45 }, { -1.4, -0.7 }, { 1.05, -0.7 }, { 1.5, 0.1 }, { 1.5, 0.75 } })
  seg(0.3, -0.7, 0.3, -0.32)
  ink.stroke(tone(WALL), W_WALL)
  local urn = { { 0.25, -0.3 }, { 0.35, -0.3 }, { 0.38, -0.2 }, { 0.33, -0.15 }, { 0.27, -0.15 }, { 0.22, -0.2 } }
  ink.poly(urn, true) ink.fill(tone(0.3))
  local function wall_y(p) return F[2] + (p[2] - F[2]) * (-1.4 - F[1]) / (p[1] - F[1]) end
  local top, bot = wall_y({ 0.3, -0.15 }), wall_y({ 0.3, -0.3 })
  ink.layer(5)
  seg(F[1], F[2], -1.4, top) seg(F[1], F[2], -1.4, bot)
  ink.stroke(ink.accent(0.2), W_THIN * 1.6, 1, false, "[1 1] 0")
  ink.layer(3)
  seg(-1.37, bot, -1.37, top) ink.stroke(tone(0.12), 2.4)          -- the shadow
  for _, x in ipairs({ -0.55, -0.8 }) do                            -- the prisoners
    ink.circle(x, -0.46, 0.055) ink.fill(tone(0.25))
    ink.moveto(x, -0.51) ink.lineto(x, -0.64) ink.lineto(x - 0.16, -0.66) ink.stroke(tone(0.25), 0.8)
  end
  ink.circle(F[1], F[2], 0.12) ink.fill(ink.accent(0.75))
  ink.poly({ { F[1] - 0.05, F[2] - 0.06 }, { F[1] + 0.05, F[2] - 0.06 }, { F[1] + 0.01, F[2] + 0.1 } }, true)
  ink.fill(ink.accent(0))
  ink.circle(1.3, 1.05, 0.07) ink.fill(ink.accent(0.2))             -- the sun
  for k = 0, 7 do
    local a = math.rad(k * 45)
    seg(1.3 + 0.1 * math.cos(a), 1.05 + 0.1 * math.sin(a), 1.3 + 0.15 * math.cos(a), 1.05 + 0.15 * math.sin(a))
  end
  ink.stroke(ink.accent(0.2), 0.5)
end

-- Dante: the nine circles from above, the seventh in three rings, the eighth in ten ditches
-- crossed by bridges, the ninth frozen; the poets' way down turns always to the left
local function inferno(s)
  local R = { 1.0, 0.9, 0.81, 0.73, 0.66, 0.6, 0.54, 0.5, 0.46 }
  for k = 0, 9 do R[#R + 1] = 0.42 - k * 0.022 end
  ink.layer(2)
  for i, r in ipairs(R) do ink.circle(0, 0, r) ink.fill(tone(0.94 - 0.16 * (i - 1) / #R)) end
  ink.circle(0, 0, 0.2) ink.fill(wash({ 0.55, 0.75, 0.95 }, 0.2))
  ink.layer(3)
  for i, r in ipairs(R) do ink.circle(0, 0, r) ink.stroke(tone(i == 1 and WALL or 0.45), i == 1 and W_WALL or W_THIN) end
  for k = 0, 5 do
    local a = math.rad(k * 60 + 15)
    seg(0.22 * math.cos(a), 0.22 * math.sin(a), 0.42 * math.cos(a), 0.42 * math.sin(a))
  end
  for _, r in ipairs({ 0.15, 0.1, 0.05 }) do ink.circle(0, 0, r) end
  ink.stroke(tone(0.4), W_THIN)
  local way = {}
  for k = 0, 120 do
    local t = k / 120
    local a = math.rad(90 + 360 * 2.25 * t)
    local r = 0.96 - 0.94 * t
    way[#way + 1] = { r * math.cos(a), r * math.sin(a) }
  end
  ink.layer(5) ink.poly(way) ink.stroke(ink.accent(0), W_RAY) ink.layer(3)
  ink.circle(0, 0.96, 0.04) ink.fill(tone(0.1))
end

-- Poe: the iron cell, the pit at its heart, and the walls closing in until the square is a
-- lozenge; the pendulum's crescent swings across the prisoner's frame
local function pit(s)
  local sq = { { 0, 1.131 }, { -1.131, 0 }, { 0, -1.131 }, { 1.131, 0 } }
  local loz = { { 0, 1.357 }, { -0.848, 0 }, { 0, -1.357 }, { 0.848, 0 } }
  ink.poly(sq, true) ink.stroke(tone(0.5), W_THIN * 1.6, 1, false, "[1.2 1] 0")
  ink.layer(2) ink.poly(loz, true) ink.fill(tone(0.86)) ink.layer(3)
  ink.poly(loz, true) ink.stroke(tone(WALL), W_WALL)
  for _, sx in ipairs({ 1, -1 }) do
    local x0, x1 = sx * 1.1, sx * 0.9
    seg(x0, 0, x1, 0) ink.stroke(ink.accent(0), 0.5)
    ink.poly({ { x1 - sx * 0.01, 0 }, { x1 + sx * 0.07, 0.035 }, { x1 + sx * 0.07, -0.035 } }, true) ink.fill(ink.accent(0))
  end
  ink.circle(0, -0.35, 0.24) ink.fill(tone(0.4))
  square(-0.09, 0.25, 0.18, 0.5) ink.stroke(tone(0.35), W_THIN * 2)
  seg(-0.42, 0.5, 0.42, 0.5) ink.stroke(tone(0.4), W_THIN * 1.6, 1, false, "[1 1] 0")
  local blade = arc(0.42, 0.42, 0.14, 200, 340, 12)
  for _, p in ipairs(arc(0.42, 0.49, 0.12, 330, 210, 12)) do blade[#blade + 1] = p end
  ink.poly(blade, true) ink.fill(ink.accent(0))
end

-- Carroll: Alice's drawing-room and the room behind the glass, where the country beyond is
-- a chessboard; light that looks straight at T's image folds back off the glass to T
local function glass(s)
  ink.layer(2)
  square(-1, -1.2, 2, 1.2) ink.fill(tone(0.9))
  for i = 0, 7 do for j = 0, 4 do
    if (i + j) % 2 == 0 then square(-1 + i * 0.25, j * 0.24, 0.25, 0.24) ink.fill(tone(0.9)) end
  end end
  ink.layer(3)
  square(-1, 0, 2, 1.2) ink.stroke(tone(0.55), W_THIN * 1.6, 1, false, "[1.2 1] 0")
  square(-1, -1.2, 2, 1.2) ink.stroke(tone(WALL), W_WALL)
  seg(-0.45, 0, 0.45, 0) ink.stroke(tone(0.4), 2.2)
  seg(-0.45, 0, 0.45, 0) ink.stroke(WHITE, 0.6)
  square(-0.3, -0.16, 0.6, 0.16) ink.stroke(tone(0.4), W_THIN * 1.6)  -- the mantelpiece
  local S, T = { -0.6, -0.8 }, { 0.5, -0.5 }
  local t = -S[2] / (-T[2] - S[2])
  local M = { S[1] + (T[1] - S[1]) * t, 0 }
  ray({ S, { T[1], -T[2] } }, false, s, true)
  ink.layer(5) ink.poly({ S, M, T }) ink.stroke(ink.accent(0), W_RAY) ink.layer(3)
  ink.circle(T[1], T[2], 0.045) ink.fill(tone(0.08))
end

-- Dumas: cells 34 and 27 in the Château d'If, Faria's tunnel between them, and the branch
-- that came up in the gallery instead of under the sea wall
local function chateau(s)
  ink.layer(2)
  square(-1, -1.2, 0.8, 0.8) ink.fill(tone(0.86))
  square(0.2, 0.3, 0.8, 0.8) ink.fill(tone(0.86))
  square(-1, 0.6, 1.1, 0.2) ink.fill(tone(0.93))
  ink.layer(3)
  square(-1, -1.2, 0.8, 0.8) square(0.2, 0.3, 0.8, 0.8) ink.stroke(tone(WALL), W_WALL)
  seg(-1, 0.6, 0.1, 0.6) seg(-1, 0.8, 0.1, 0.8) ink.stroke(tone(0.45), W_THIN * 1.6)
  ink.poly({ { 0.45, 0.3 }, { 0.45, 0.05 }, { 0.1, 0.05 }, { 0.1, -0.25 }, { -0.45, -0.25 }, { -0.45, -0.4 } })
  ink.poly({ { 0.1, 0.05 }, { -0.5, 0.05 }, { -0.5, 0.6 } })
  ink.stroke(ink.accent(0), W_RAY * 1.6, 1, false, "[1.2 0.9] 0")
  local sea = {}
  for k = 0, 48 do local x = -1 + k / 24 sea[#sea + 1] = { x, -1.42 + 0.03 * math.sin(x * 22) } end
  ink.poly(sea) ink.stroke(tone(0.45), W_THIN * 1.6)
  for _, c in ipairs({ { -0.6, -0.8 }, { 0.6, 0.7 } }) do ink.circle(c[1], c[2], 0.04) ink.fill(tone(0.1)) end
end

local LIT = {
  { draw = masque, box = { -1.06, -2.83, 1.06, 2.83 }, caption = "\\textit{The Masque of the Red Death}\\\\Poe, 1842" },
  { draw = phantom, box = { -2.5, -2.6, 2.5, 2.6 }, caption = "\\textit{The Phantom of the Opera}\\\\Leroux, 1910" },
  { draw = babel, box = { -1, -2.25, 1, 2.25 }, caption = "\\textit{The Library of Babel}\\\\Borges, 1941" },
  { draw = cave, box = { -1.45, -0.75, 1.55, 1.2 }, caption = "The cave, \\textit{Republic} VII\\\\Plato, c.~375 BC" },
  { draw = inferno, box = { -1, -1, 1, 1 }, caption = "\\textit{Inferno}\\\\Dante, c.~1320" },
  { draw = pit, box = { -1.15, -1.36, 1.15, 1.36 }, caption = "\\textit{The Pit and the Pendulum}\\\\Poe, 1842" },
  { draw = glass, box = { -1, -1.2, 1, 1.2 }, caption = "\\textit{Through the Looking-Glass}\\\\Carroll, 1871" },
  { draw = chateau, box = { -1, -1.48, 1, 1.1 }, caption = "\\textit{The Count of Monte Cristo}\\\\Dumas, 1844" },
}

-- the light that threads the margin column: corner to corner, bouncing between its sides
local function thread(x0, y0, x1, y1)
  local W, H = x1 - x0, y1 - y0
  local n = max(1, floor(H / (1.7 * W) + 0.5))
  local pts = {}
  for k = 0, n do pts[#pts + 1] = { k % 2 == 0 and x0 or x1, y1 - H * k / n } end
  ink.layer(1)
  ink.poly(pts) ink.stroke(ink.accent(0.3), 0.4, 1, false, "[0.4 1.8] 0")
  ink.layer(3)
end

-- the head rule's fleuron: a small copper A star; returns the page point where the rule starts
local function fleuron(rng, s)
  ink.push() ink.scale(s)
  star(rng, 0.5, true)()
  local c = ink.accent(0)
  ink.moveto(0.5, 0) ink.lineto(2.0, 0) ink.stroke(c, 0.4)
  local rx, ry = ink.to_page(2.0, 0)
  ink.pop()
  return rx, ry
end
M.flora = { hedera = fleuron }

-- ---------------------------------------------------------------- the page
function M.page(g, grow)
  local layout = ink.rng(g.seed * 7919 + 41)
  ink.set_transform(ink.page_transform(g.mirror and g.pw))
  local D = g.density or 1
  local _, col, foot, spill = grow.regions(g, layout)
  local regions = { col, foot, spill }
  local fld = grow.field(regions)
  local gx, gy, free, disc, free_at = fld.x, fld.y, fld.free, fld.disc, fld.free_at
  disc(g.colright - 0.5, g.headrule + 0.1, 0.7, 1)         -- the head rule's fleuron
  local function place(x, y, fn) ink.layer(3) ink.push() ink.translate(x, y) fn() ink.pop() end
  thread(col[1] + 0.15, col[2] + 0.2, col[3] - 0.25, col[4] - 0.3)

  -- 1. Peyton's room in the corner, on the pages where a part begins
  local cw = col[3] - col[1]
  local opens = false
  for _, mk in ipairs(g.marks or {}) do if mk.kind == "heading" and mk.arg == 1 then opens = true end end
  if opens then
    local R = min(1.7, cw * 0.45)
    local x, y = col[1] + R + 0.1, col[2] + R + 0.15
    if free_at(x, y) >= R * 0.9 then place(x, y, room22(R)) disc(x, y, R, 1) end
  end

  -- 2. a copper A star beside each section heading
  for _, mk in ipairs(g.marks or {}) do
    if mk.kind == "heading" then
      local R = mk.arg == 1 and 0.32 or 0.24
      local x, y = g.colright - R - 0.2, mk.y + 0.15
      if free_at(x, y) >= R + 0.05 then place(x, y, star(layout, R, true)) disc(x, y, R + 0.15, 1) end
    end
  end

  -- 3. a famous dark room from literature, a different one on each page, with its caption
  local captions = {}
  do
    local lit = LIT[(tex.count[0] - 1) % #LIT + 1]
    local b = lit.box
    local bw, bh = b[3] - b[1], b[4] - b[2]
    local s = min(2 * (cw / 2 - 0.35) / bw, 4.4 / bh)
    local hw, hh = s * bw / 2, s * bh / 2 + 0.3            -- half sizes, with the caption below
    -- the spot where the whole drawing and its caption stay clearest
    local best, bx, by = 0, nil, nil
    for i = 1, #gx do
      if gx[i] < col[3] and gy[i] > col[2] + hh and gy[i] < col[4] - hh then
        local f = math.huge
        for yy = gy[i] - hh + hw, gy[i] + hh - hw, 0.3 do f = min(f, free_at(gx[i], yy)) end
        f = min(f, free_at(gx[i], gy[i] - hh + hw), free_at(gx[i], gy[i] + hh - hw)) * layout.range(0.9, 1.1)
        if f > best then best, bx, by = f, gx[i], gy[i] end
      end
    end
    if bx and best > hw then
      local cy = by + 0.3
      place(bx, cy, function() ink.scale(s) ink.translate(-(b[1] + b[3]) / 2, -(b[2] + b[4]) / 2) lit.draw(s) end)
      captions[1] = { x = bx, y = cy - s * bh / 2 - 0.12, text = lit.caption, small = true }
      for yy = by - hh, by + hh, 0.25 do disc(bx, yy, hw + 0.25, 1) end
    end
  end

  -- ghosts: one or two large pale pieces of the tiling in open space, behind what fills it later
  for _ = 1, layout.int(1, 2) do
    local i = layout.int(1, #gx)
    for _ = 1, 40 do
      if gx[i] < col[3] and free[i] > 1.2 then break end
      i = layout.int(1, #gx)
    end
    if gx[i] < col[3] and free[i] > 1.2 then
      local R = layout.range(1.3, 1.8)
      local fn = layout.chance(0.5) and tiles(layout, R) or star(layout, R)
      local turn = layout.chance(0.5) and 45 or 0
      local old = ink.set_lift(0.8)
      ink.layer(1)
      ink.poly({ { col[1], col[2] }, { col[3], col[2] }, { col[3], col[4] }, { col[1], col[4] } }, true) ink.clip()
      ink.push() ink.translate(gx[i], gy[i]) ink.rotate(turn) fn() ink.pop()
      ink.unclip()
      ink.set_lift(old)
    end
  end

  -- 4. the corridor along the bottom
  if D >= 0.1 then
    local h = min(0.42, (foot[4] - foot[2]) * 0.8)
    local y0 = (foot[2] + foot[4]) / 2 - h / 2
    corridor(foot[1] + 0.2, y0, foot[3] - 0.2, h)
    for x = foot[1] + 0.2, foot[3] - 0.2, h * 0.5 do disc(x, y0 + h / 2, h, 1) end
  end

  -- 5. the rest, largest hole first
  local area = 0
  for _, r in ipairs(regions) do area = area + (r[3] - r[1]) * (r[4] - r[2]) end
  local NMAX = floor(D * area / 8 + 0.5)
  local MINF = 0.32 / sqrt(D)
  for _ = 1, NMAX do
    local best, bi = -1, nil
    for i = 1, #gx do
      local v = free[i] * layout.range(0.85, 1.15)
      if v > best then best, bi = v, i end
    end
    if not bi or free[bi] < MINF then break end
    local f, x, y = free[bi], gx[bi], gy[bi]
    local u = layout.u()
    if f > 0.75 then
      local R = min(f * 0.92, 1.3)
      local fn = u < 0.5 and small_room(layout, R) or u < 0.7 and unfold(layout, R)
        or u < 0.85 and tiles(layout, R) or star(layout, R * 0.8)
      place(x, y, fn) disc(x, y, R + 0.15, 1)
    elseif f > 0.36 then
      local R = f * layout.range(0.75, 0.92)
      local fn = u < 0.3 and star(layout, R) or u < 0.55 and cells(layout, R) or u < 0.75 and tiles(layout, R)
        or small_room(layout, R)
      place(x, y, fn) disc(x, y, R + 0.12, 1)
    elseif f > 0.2 then
      local R = min(f, 0.3) * layout.range(0.7, 0.95)
      place(x, y, u < 0.6 and star(layout, R) or cells(layout, R)) disc(x, y, R + 0.1, 1)
    else
      local r = min(f, 0.12) * layout.range(0.35, 0.6)
      local px, py = layout.int(0, 1), layout.int(0, 1)
      local c = layout.chance(0.25) and ink.accent(0) or tone(layout.range(0.15, 0.45))
      place(x, y, function() ink.push() ink.scale(r) ink.translate(-px, -py) mark(px, py, 1, c) ink.pop() end)
      disc(x, y, max(r * 2.5, 0.15), 1)
    end
  end

  ink.flush()
  return { captions = captions }
end

return M
