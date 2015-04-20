import mcp3008

def getData(channel):
    return mcp3008.getTenBit(channel)
