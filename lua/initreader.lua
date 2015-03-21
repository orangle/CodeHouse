-- INI Reader

function NewIniReader()
    local reader = {};
    function reader:Read(fName)
        self.root = {};
        self.reading_section = "";
        for line in io.lines(fName) do
            if startsWith(line, "[") then
                local section = string.sub(line,2,-2);
                self.root[section] = {};
                self.reading_section = section;
            elseif not startsWith(line, ";") then
                if self.reading_section then
                    local var,val = line:split("=");
                    local var,val = var:trim(), val:trim();
                    print("["..var.."] ["..val.."]")
                    if string.find(val, ";") then
                        val,comment = val:split(";");
                        val = val:trim();
                    end
                    self.root[self.reading_section] = self.root[self.reading_section] or {};
                    self.root[self.reading_section][var] = val;
                else
                    return error("No element set for setting");
                end
            end
        end
    end

    -- get value 'Key' from section
    function reader:GetValue(Section, Key)
        return self.root[Section][Key];
    end

    -- get keys from a section
    function reader:GetKeys(Section)
        return self.root[Section];
    end

    -- return the object
    return reader;
end

-- String functions from Haywoods DROPP Script..
function startsWith(text,prefix)
    return string.sub(text, 1, string.len(prefix)) == prefix
end

function string:split(sep)
    return self:match("([^" .. sep .. "]+)[" .. sep .. "]+(.+)")
end

function string:trim()
    return self:match("^%s*(.-)%s*$")
end


-----------------
reader = NewIniReader()
reader:Read("./settings.ini")
value = reader:GetValue("default", "VERSION")








