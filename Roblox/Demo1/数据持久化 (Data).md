```lua
local ProfileService = require(script.ProfileService)

local Profiles = {}

local DataManager = {}

function DataManager:Get(player)
	local profile = Profiles[player]
	
	if profile then
		return profile
	end
end

return DataManager
```

