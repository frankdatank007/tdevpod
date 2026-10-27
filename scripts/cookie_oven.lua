-- cookie_oven.lua: bake a tray of cookies with a very hot arrow (never runs)
local Oven = {}
Oven.__index = Oven

function Oven.new(temp)
  return setmetatable({ temp = temp, tray = {} }, Oven)
end

function Oven:add(cookie)
  table.insert(self.tray, cookie)
end

local function bar(pct)
  local filled = math.floor(pct / 5)
  if filled >= 20 then return "[" .. string.rep("=", 20) .. "]" end
  return "[" .. string.rep("=", filled) .. ">" .. string.rep(".", 19 - filled) .. "]"
end

local oven = Oven.new(350)
for _, name in ipairs({ "chip", "sprinkle", "dino-shaped" }) do
  oven:add(name)
end

for pct = 0, 100, 5 do
  io.write(string.format("\r%s %3d%%  baking %d cookies", bar(pct), pct, #oven.tray))
end
print("\nding! cookies are ready (and still too hot)")

-- $ lua cookie_oven.lua

-- ── output ────────────────────────────────────────────
[....................]   0%  preheating the oven
[>...................]   5%  preheating the oven
[=>..................]  10%  preheating the oven
[==>.................]  15%  preheating the oven
[===>................]  20%  preheating the oven
[====>...............]  25%  preheating the oven
[=====>..............]  30%  preheating the oven
[======>.............]  35%  preheating the oven
[=======>............]  40%  preheating the oven
[========>...........]  45%  preheating the oven
[=========>..........]  50%  preheating the oven
[==========>.........]  55%  preheating the oven
[===========>........]  60%  preheating the oven
[============>.......]  65%  preheating the oven
[=============>......]  70%  preheating the oven
[==============>.....]  75%  preheating the oven
[===============>....]  80%  preheating the oven
[================>...]  85%  preheating the oven
[=================>..]  90%  preheating the oven
[==================>.]  95%  preheating the oven
[====================] 100%  preheating the oven
✔ oven is 350 degrees of cozy
◐ spinning the sprinkle jar...
◓ spinning the sprinkle jar...
◑ spinning the sprinkle jar...
◒ spinning the sprinkle jar...
◐ spinning the sprinkle jar...
◓ spinning the sprinkle jar...
◑ spinning the sprinkle jar...
◒ spinning the sprinkle jar...
◐ spinning the sprinkle jar...
◓ spinning the sprinkle jar...
◑ spinning the sprinkle jar...
◒ spinning the sprinkle jar...
◐ spinning the sprinkle jar...
◓ spinning the sprinkle jar...
◑ spinning the sprinkle jar...
◒ spinning the sprinkle jar...
→ next up!
[....................]   0%  baking 3 cookies
[>...................]   5%  baking 3 cookies
[=>..................]  10%  baking 3 cookies
[==>.................]  15%  baking 3 cookies
[===>................]  20%  baking 3 cookies
[====>...............]  25%  baking 3 cookies
[=====>..............]  30%  baking 3 cookies
[======>.............]  35%  baking 3 cookies
[=======>............]  40%  baking 3 cookies
[========>...........]  45%  baking 3 cookies
[=========>..........]  50%  baking 3 cookies
[==========>.........]  55%  baking 3 cookies
[===========>........]  60%  baking 3 cookies
[============>.......]  65%  baking 3 cookies
[=============>......]  70%  baking 3 cookies
[==============>.....]  75%  baking 3 cookies
[===============>....]  80%  baking 3 cookies
[================>...]  85%  baking 3 cookies
[=================>..]  90%  baking 3 cookies
[==================>.]  95%  baking 3 cookies
[====================] 100%  baking 3 cookies
→ next up!
▖ waiting for cookies to cool...
▘ waiting for cookies to cool...
▝ waiting for cookies to cool...
▗ waiting for cookies to cool...
▖ waiting for cookies to cool...
▘ waiting for cookies to cool...
▝ waiting for cookies to cool...
▗ waiting for cookies to cool...
▖ waiting for cookies to cool...
▘ waiting for cookies to cool...
▝ waiting for cookies to cool...
▗ waiting for cookies to cool...
✔ cookies: 3, crumbs: lots
