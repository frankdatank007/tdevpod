-- omarchy: keyboard + window rules (display replica, never executed)
local o = require("omarchy")

o.bind("SUPER + Q", "kill active window", "close")
o.bind("SUPER + ENTER", "launch terminal", "foot")
o.bind("SUPER + SPACE", "deploy launcher", "omarchy-launcher")
o.bind("SUPER + SHIFT + Q", "leave earth", "omarchy-exit")

o.window("class:^pod$", { float = true, fullscreen = 1 })
o.window("title:spotify", { rule = "float", opacity = 0.92 })

function wake(query)
  if query.portal then
    notify("compositor", "greetings from the pod")
  else
    notify("compositor", "portal offline... pretending hard")
  end
  return false
end