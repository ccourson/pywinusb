#
class UsagePage(object):
    """Translate usage name between numeric and string values.
    So, str() or int() can be applied to get desired value
    """
    __usageMapStringKeys = {
        #Page ID Page Name Section or Document
        #^0*\([0-9\-a-fA-F]+\)\( \)\(.*\) used to convert hid table
        "Generic Desktop": 1,
        "Simulation": 2,
        "VR": 3,
        "Sport": 4,
        "Game": 5,
        "Generic Device": 6,
        "Keyboard/Keypad": 7,
        "LED": 8,
        "Button": 9,
        "Ordinal": 0xA,
        "Telephony": 0xB,
        "Consumer": 0xC,
        "Digitizer": 0xD,
        "PID": 0xF, #Physical Interface Device (force feedback and related)
        "Unicode": 0x10,
        "Alphanumeric Display": 0x14,
        "Medical Instrument": 0x40,
        # point of sale devices
        "Bar Code Scanner": 0x8C,
        "Scale": 0x8D,
        "MSR": 0x8E, #Magnetic Stripe Reading (MSR) Devices
        "Reserved Point of Sale": 0x8F,
        "Camera Control": 0x90, #Image class devices
        "Arcade": 0x91, #arcade and coinop related devices
    }

    # oposite key/value arrangement
    __usageMapNumberKeys = dict([(b,a) for (a,b) in __usageMapStringKeys.items()])
    #important: items are sorted!
    #range, name
    __rangeUsages = [\
        (0x11, 0x13, "Reserved"),
        (0x15, 0x3f,  "Reserved"),
        (0x41, 0x7F,   "Reserved"),
        (0x80, 0x83,  "Monitor"), #Monitor Devices
        (0x84, 0x87,   "Power"), #Power Devices
        (0x88, 0x8B,  "Reserved"),
        (0x92, 0xFEFF, "Reserved"),
        (0xFF00, 0xFFFF, "Vendor-defined"),
        ]
    
    def __init__(self, page):
        if isinstance(page, str):
            if page not in self.__usageMapStringKeys:
                raise KeyError("Wrong page name or page name resoves to value range")
        elif isinstance(page, int) or isinstance(page, long):
            if (page < 0 or page > 0xffff):
                raise ValueError("Wrong page range (0~0xffff)")
        else:
            raise TypeError("Usage page referenced only by name (str) or value (int)")
        self.page = page
        
    def __int__(self):
        if isinstance(self.page, str):
            name = self.page
        elif isinstance(self.page, int):
            return self.page
        else:
            return 0
        # return name
        return self.__usageMapStringKeys.get(name, 0)
    
    def __str__(self):
        if isinstance(self.page, str):
            return self.page
        elif isinstance(self.page, int):
            if self.page in self.__usageMapNumberKeys:
                return self.__usageMapNumberKeys[self.page]
            else:
                #lookup within ranges
                for lowLimit, highLimit, name in self.__rangeUsages:
                    if lowLimit <= self.page <= highLimit:
                        return name
        return ""
            
# ***********************************
#
#
[\
    CP,
    CA,
    DV,
    CL, 
    OSC,
    OOC,
    DV,
    DF,
    Multiplier,
    RTC,
    Sel,
    MC,
    NAry,
    LC,
    SV, #15
    US,
    UM,
    SF,
    BufferedBytes,
] = range(19)
    
class HidUsage(object):
    #usage tables
    #done finding regex:
    #    ^0*\([0-9\-a-fA-F]+\)\( \)\(\D*\)\( .*\)\( \d+\.\d+\)$
    #    ^0*\([0-9\-a-fA-F]+\)\( \)\(\D*\)\( .*\)\( \d+\.\d+\.*\d*\)$
    #and replacing by:
    #    0x\1: ("\3", \4),
    Usages = {
    0x01: { #generic desktop page
        #UsageID: ("Usage Name", UsageType),
        #00 Undefined
        0x1: ("Pointer", CP),
        0x2: ("Mouse", CA),
        #03 Reserved
        0x4: ("Joystick", CA),
        0x5: ("Game Pad", CA),
        0x6: ("Keyboard", CA),
        0x7: ("Keypad", CA),
        0x8: ("Multi-axis Controller", CA),
        0x9: ("Tablet PC System Controls", CA),
        #0A-2F Reserved
        0x30: ("X", DV),
        0x31: ("Y", DV),
        0x32: ("Z", DV),
        0x33: ("Rx", DV),
        0x34: ("Ry", DV),
        0x35: ("Rz", DV),
        0x36: ("Slider", DV),
        0x37: ("Dial", DV),
        0x38: ("Wheel", DV),
        0x39: ("Hat switch", DV),
        0x3A: ("Counted Buffer", CL),
        0x3B: ("Byte Count", DV),
        0x3C: ("Motion Wakeup", OSC),
        0x3D: ("Start", OOC),
        0x3E: ("Select", OOC),
        #3F Reserved
        0x40: ("Vx", DV),
        0x41: ("Vy", DV),
        0x42: ("Vz", DV),
        0x43: ("Vbrx", DV),
        0x44: ("Vbry", DV),
        0x45: ("Vbrz", DV),
        0x46: ("Vno", DV),
        #0x47: ("Feature Notification", DV,DF),#
        0x47: ("Feature Notification", DF),#
        0x48: ("Resolution", Multiplier),
        #49-7F Reserved
        0x80: ("System Control", CA),
        0x81: ("System Power Down", OSC),
        0x82: ("System Sleep", OSC),
        0x83: ("System Wake Up", OSC),
        0x84: ("System Context Menu", OSC),
        0x85: ("System Main Menu", OSC),
        0x86: ("System App Menu", OSC),
        0x87: ("System Menu Help", OSC),
        0x88: ("System Menu Exit", OSC),
        0x89: ("System Menu Select", OSC),
        0x8A: ("System Menu Right", RTC),
        0x8B: ("System Menu Left", RTC),
        0x8C: ("System Menu Up", RTC),
        0x8D: ("System Menu Down", RTC),
        0x8E: ("System Cold Restart", OSC),
        0x8F: ("System Warm Restart", OSC),
        0x90: ("D-pad Up", OOC),
        0x91: ("D-pad Down", OOC),
        0x92: ("D-pad Right", OOC),
        0x93: ("D-pad Left", OOC),
        #94-9F Reserved
        0xA0: ("System Dock", OSC),
        0xA1: ("System Undock", OSC),
        0xA2: ("System Setup", OSC),
        0xA3: ("System Break", OSC),
        0xA4: ("System Debugger Break", OSC),
        0xA5: ("Application Break", OSC),
        0xA6: ("Application Debugger Break", OSC),
        0xA7: ("System Speaker Mute", OSC),
        0xA8: ("System Hibernate", OSC),
        #A9-AF Reserved
        0xB0: ("System Display Invert", OSC),
        0xB1: ("System Display Internal", OSC),
        0xB2: ("System Display External", OSC),
        0xB3: ("System Display Both", OSC),
        0xB4: ("System Display Dual", OSC),
        0xB5: ("System Display Toggle Int/Ext", OSC),
        0xB6: ("System Display Swap", OSC),
        0xB7: ("System Display LCD Autoscale", OSC),
        #B8-FFFF Reserved
        },
    #simulation controls page
    0x02 : {
        #00 Undefined
        0x1: ("Flight Simulation Device", CA),
        0x2: ("Automobile Simulation Device", CA),
        0x3: ("Tank Simulation Device", CA),
        0x4: ("Spaceship Simulation Device", CA),
        0x5: ("Submarine Simulation Device", CA),
        0x6: ("Sailing Simulation Device", CA),
        0x7: ("Motorcycle Simulation Device", CA),
        0x8: ("Sports Simulation Device", CA),
        0x9: ("Airplane Simulation Device", CA),
        0xA: ("Helicopter Simulation Device", CA),
        0xB: ("Magic Carpet Simulation Device", CA),
        0xC: ("Bicycle Simulation Device", CA),
        #0D - 1F Reserved
        0x20: ("Flight Control Stick", CA),
        0x21: ("Flight Stick", CA),
        0x22: ("Cyclic Control", CP),
        0x23: ("Cyclic Trim", CP),
        0x24: ("Flight Yoke", CA),
        0x25: ("Track Control", CP),
        #26 - AF Reserved
        0xB0: ("Aileron", DV),
        0xB1: ("Aileron Trim", DV),
        0xB2: ("Anti-Torque Control", DV),
        0xB3: ("Autopilot Enable", OOC),
        0xB4: ("Chaff Release", OSC),
        0xB5: ("Collective Control", DV),
        0xB6: ("Dive Brake", DV),
        0xB7: ("Electronic Countermeasures", OOC),
        0xB8: ("Elevator", DV),
        0xB9: ("Elevator Trim", DV),
        0xBA: ("Rudder", DV),
        0xBB: ("Throttle", DV),
        0xBC: ("Flight Communications", OOC),
        0xBD: ("Flare Release", OSC),
        0xBE: ("Landing Gear", OOC),
        0xBF: ("Toe Brake", DV),
        0xC0: ("Trigger", MC),
        0xC1: ("Weapons Arm", OOC),
        0xC2: ("Weapons Select", OSC),
        0xC3: ("Wing Flaps", DV),
        0xC4: ("Accelerator", DV),
        0xC5: ("Brake", DV),
        0xC6: ("Clutch", DV),
        0xC7: ("Shifter", DV),
        0xC8: ("Steering", DV),
        0xC9: ("Turret Direction", DV),
        0xCA: ("Barrel Elevation", DV),
        0xCB: ("Dive Plane", DV),
        0xCC: ("Ballast", DV),
        0xCD: ("Bicycle Crank", DV),
        0xCE: ("Handle Bars", DV),
        0xCF: ("Front Brake", DV),
        0xD0: ("Rear Brake", DV),
        #D1-FFFF Reserved
        },
    #VR controls page
    0x03 : {
        0x1: ("Belt", CA),
        0x2: ("Body Suit", CA),
        0x3: ("Flexor", CP),
        0x4: ("Glove", CA),
        0x5: ("Head Tracker", CP),
        0x6: ("Head Mounted Display", CA),
        0x7: ("Hand Tracker", CA),
        0x8: ("Oculometer", CA),
        0x9: ("Vest", CA),
        0xA: ("Animatronic Device", CA),
        #0B-1F Reserved
        0x20: ("Stereo Enable", OOC),
        0x21: ("Display Enable", OOC),
        #22-FFFF Reserved
        },
    0x04: {
        0x1: ("Baseball Bat", CA),
        0x2: ("Golf Club", CA),
        0x3: ("Rowing Machine", CA),
        0x4: ("Treadmill", CA),
        #05-2F Reserved
        0x30: ("Oar", DV),
        0x31: ("Slope", DV),
        0x32: ("Rate", DV),
        0x33: ("Stick Speed", DV),
        0x34: ("Stick Face Angle", DV),
        0x35: ("Stick Heel/Toe", DV),
        0x36: ("Stick Follow Through", DV),
        0x37: ("Stick Tempo", DV),
        0x38: ("Stick Type", NAry),
        0x39: ("Stick Height", DV),
        #3A-4F Reserved
        0x50: ("Putter", Sel),
        0x51: ("1 Iron", Sel),
        0x52: ("2 Iron", Sel),
        0x53: ("3 Iron", Sel),
        0x54: ("4 Iron", Sel),
        0x55: ("5 Iron", Sel),
        0x56: ("6 Iron", Sel),
        0x57: ("7 Iron", Sel),
        0x58: ("8 Iron", Sel),
        0x59: ("9 Iron", Sel),
        0x5A: ("10 Iron", Sel),
        0x5B: ("11 Iron", Sel),
        0x5C: ("Sand Wedge", Sel),
        0x5D: ("Loft Wedge", Sel),
        0x5E: ("Power Wedge", Sel),
        0x5F: ("1 Wood", Sel),
        0x60: ("3 Wood", Sel),
        0x61: ("5 Wood", Sel),
        0x62: ("7 Wood", Sel),
        0x63: ("9 Wood", Sel),
        #64-FFFF Reserved
        },
    0x05: {
        0x1: ("3D Game Controller", CA),
        0x2: ("Pinball Device", CA),
        0x3: ("Gun Device", CA),
        #04-1F Reserved
        0x20: ("Point of View", CP),
        0x21: ("Turn Right/Left", DV),
        0x22: ("Pitch Forward/Backward", DV),
        0x23: ("Roll Right/Left", DV),
        0x24: ("Move Right/Left", DV),
        0x25: ("Move Forward/Backward", DV),
        0x26: ("Move Up/Down", DV),
        0x27: ("Lean Right/Left", DV),
        0x28: ("Lean Forward/Backward", DV),
        0x29: ("Height of POV", DV),
        0x2A: ("Flipper", MC),
        0x2B: ("Secondary Flipper", MC),
        0x2C: ("Bump", MC),
        0x2D: ("New Game", OSC),
        0x2E: ("Shoot Ball", OSC),
        0x2F: ("Player", OSC),
        0x30: ("Gun Bolt", OOC),
        0x31: ("Gun Clip", OOC),
        0x32: ("Gun Selector", NAry),
        0x33: ("Gun Single Shot", Sel),
        0x34: ("Gun Burst", Sel),
        0x35: ("Gun Automatic", Sel),
        0x36: ("Gun Safety", OOC),
        0x37: ("Gamepad Fire/Jump", CL),
        0x39: ("Gamepad Trigger", CL),
        #3A-FFFF Reserved
        },
    #game device controls
    0x06: {
        #01-1F Reserved
        0x20: ("Battery Strength", DV),
        0x21: ("Wireless Channel", DV),
        0x22: ("Wireless ID", DV),
        0x23: ("Discover Wireless Control", OSC),
        0x24: ("Security Code Character Entered", OSC),
        0x25: ("Security Code Character Erased", OSC),
        0x26: ("Security Code Cleared", OSC),
        #27-FFFF Reserved
        },
    #7 keyboard/keypad... not yet
    #8 LED page
    0x08: {
        0x1: ("Num Lock", OOC),
        0x2: ("Caps Lock", OOC),
        0x3: ("Scroll Lock", OOC),
        0x4: ("Compose", OOC),
        0x5: ("Kana", OOC),
        0x6: ("Power", OOC),
        0x7: ("Shift", OOC),
        0x8: ("Do Not Disturb", OOC),
        0x9: ("Mute", OOC),
        0xA: ("Tone Enable", OOC),
        0xB: ("High Cut Filter", OOC),
        0xC: ("Low Cut Filter", OOC),
        0xD: ("Equalizer Enable", OOC),
        0xE: ("Sound Field On", OOC),
        0xF: ("Surround On", OOC),
        0x10: ("Repeat", OOC),
        0x11: ("Stereo", OOC),
        0x12: ("Sampling Rate Detect", OOC),
        0x13: ("Spinning", OOC),
        0x14: ("CAV", OOC),
        0x15: ("CLV", OOC),
        0x16: ("Recording Format Detect", OOC),
        0x17: ("Off-Hook", OOC),
        0x18: ("Ring", OOC),
        0x19: ("Message Waiting", OOC),
        0x1A: ("Data Mode", OOC),
        0x1B: ("Battery Operation", OOC),
        0x1C: ("Battery OK", OOC),
        0x1D: ("Battery Low", OOC),
        0x1E: ("Speaker", OOC),
        0x1F: ("Head Set", OOC),
        0x20: ("Hold", OOC),
        0x21: ("Microphone", OOC),
        0x22: ("Coverage", OOC),
        0x23: ("Night Mode", OOC),
        0x24: ("Send Calls", OOC),
        0x25: ("Call Pickup", OOC),
        0x26: ("Conference", OOC),
        0x27: ("Stand-by", OOC),
        0x28: ("Camera On", OOC),
        0x29: ("Camera Off", OOC),
        0x2A: ("On-Line", OOC),
        0x2B: ("Off-Line", OOC),
        0x2C: ("Busy", OOC),
        0x2D: ("Ready", OOC),
        0x2E: ("Paper-Out", OOC),
        0x2F: ("Paper-Jam", OOC),
        0x30: ("Remote", OOC),
        0x31: ("Forward", OOC),
        0x32: ("Reverse", OOC),
        0x33: ("Stop", OOC),
        0x34: ("Rewind", OOC),
        0x35: ("Fast Forward", OOC),
        0x36: ("Play", OOC),
        0x37: ("Pause", OOC),
        0x38: ("Record", OOC),
        0x39: ("Error", OOC),
        0x3A: ("Usage Selected Indicator", US),
        0x3B: ("Usage In Use Indicator", US),
        0x3C: ("Usage Multi Mode Indicator", UM),
        0x3D: ("Indicator On", Sel),
        0x3E: ("Indicator Flash", Sel),
        0x3F: ("Indicator Slow Blink", Sel),
        0x40: ("Indicator Fast Blink", Sel),
        0x41: ("Indicator Off", Sel),
        0x42: ("Flash On Time", DV),
        0x43: ("Slow Blink On Time", DV),
        0x44: ("Slow Blink Off Time", DV),
        0x45: ("Fast Blink On Time", DV),
        0x46: ("Fast Blink Off Time", DV),
        0x47: ("Usage Indicator Color", UM),
        0x48: ("Indicator Red", Sel),
        0x49: ("Indicator Green", Sel),
        0x4A: ("Indicator Amber", Sel),
        0x4B: ("Generic Indicator", OOC),
        0x4C: ("System Suspend", OOC),
        0x4D: ("External Power Connected", OOC),
        #4E-FFFF Reserved
        },
    #9, button page, handled with code
    # as the usage names map directly to the id (consistently)
    # i.e. usageID=12, maps to button 12
    #0xa, ordinal page handled with code (Instance naming)
    #0xb, telephony page
    0xb : {
        0x1: ("Phone", CA),
        0x2: ("Answering Machine", CA),
        0x3: ("Message Controls", CL),
        0x4: ("Handset", CL),
        0x5: ("Headset", CL),
        0x6: ("Telephony Key Pad", NAry),
        0x7: ("Programmable Button", NAry),
        #08-1F Reserved
        0x20: ("Hook Switch", OOC),
        0x21: ("Flash", MC),
        0x22: ("Feature", OSC),
        0x23: ("Hold", OOC),
        0x24: ("Redial", OSC),
        0x25: ("Transfer", OSC),
        0x26: ("Drop", OSC),
        0x27: ("Park", OOC),
        0x28: ("Forward Calls", OOC),
        0x29: ("Alternate Function", MC),
        0x2A: ("Line OSC,", NAry),
        0x2B: ("Speaker Phone", OOC),
        0x2C: ("Conference", OOC),
        0x2D: ("Ring Enable", OOC),
        0x2E: ("Ring Select", OSC),
        0x2F: ("Phone Mute", OOC),
        0x30: ("Caller ID", MC),
        0x31: ("Send", OOC),
        #32-4F Reserved
        0x50: ("Speed Dial", OSC),
        0x51: ("Store Number", OSC),
        0x52: ("Recall Number", OSC),
        0x53: ("Phone Directory", OOC),
        #54-6F Reserved
        0x70: ("Voice Mail", OOC),
        0x71: ("Screen Calls", OOC),
        0x72: ("Do Not Disturb", OOC),
        0x73: ("Message", OSC),
        0x74: ("Answer On/Off", OOC),
        #75-8F Reserved
        0x90: ("Inside Dial Tone", MC),
        0x91: ("Outside Dial Tone", MC),
        0x92: ("Inside Ring Tone", MC),
        0x93: ("Outside Ring Tone", MC),
        0x94: ("Priority Ring Tone", MC),
        0x95: ("Inside Ringback", MC),
        0x96: ("Priority Ringback", MC),
        0x97: ("Line Busy Tone", MC),
        0x98: ("Reorder Tone", MC),
        0x99: ("Call Waiting Tone", MC),
        0x9A: ("Confirmation Tone 1", MC),
        0x9B: ("Confirmation Tone 2", MC),
        0x9C: ("Tones Off", OOC),
        0x9D: ("Outside Ringback", MC),
        0x9E: ("Ringer", OOC),
        #9E-AF Reserved
        0xB0: ("Phone Key 0", Sel),
        0xB1: ("Phone Key 1", Sel),
        0xB2: ("Phone Key 2", Sel),
        0xB3: ("Phone Key 3", Sel),
        0xB4: ("Phone Key 4", Sel),
        0xB5: ("Phone Key 5", Sel),
        0xB6: ("Phone Key 6", Sel),
        0xB7: ("Phone Key 7", Sel),
        0xB8: ("Phone Key 8", Sel),
        0xB9: ("Phone Key 9", Sel),
        0xBA: ("Phone Key Star", Sel),
        0xBB: ("Phone Key Pound", Sel),
        0xBC: ("Phone Key A", Sel),
        0xBD: ("Phone Key B", Sel),
        0xBE: ("Phone Key C", Sel),
        0xBF: ("Phone Key D", Sel),
        #C0-FFFF Reserved
                },
    #0xc, generic consumer control device
    0xc: {
        0x1: ("Consumer Control", CA),
        0x2: ("Numeric Key Pad", NAry),
        0x3: ("Programmable Buttons", NAry),
        0x4: ("Microphone", CA),
        0x5: ("Headphone", CA),
        0x6: ("Graphic Equalizer", CA),
        #07-1F Reserved
        0x20: ("+10", OSC),
        0x21: ("+100", OSC),
        0x22: ("AM/PM", OSC),
        #23-3F Reserved
        0x30: ("Power", OOC),
        0x31: ("Reset", OSC),
        0x32: ("Sleep", OSC),
        0x33: ("Sleep After", OSC),
        0x34: ("Sleep Mode", RTC),
        0x35: ("Illumination", OOC),
        0x36: ("Function Buttons", NAry),
        #37-3F Reserved
        0x40: ("Menu", OOC),
        0x41: ("Menu Pick", OSC),
        0x42: ("Menu Up", OSC),
        0x43: ("Menu Down", OSC),
        0x44: ("Menu Left", OSC),
        0x45: ("Menu Right", OSC),
        0x46: ("Menu Escape", OSC),
        0x47: ("Menu Value Increase", OSC),
        0x48: ("Menu Value Decrease", OSC),
        #49-5F Reserved
        0x60: ("Data On Screen", OOC),
        0x61: ("Closed Caption", OOC),
        0x62: ("Closed Caption Select", OSC),
        0x63: ("VCR/TV", OOC),
        0x64: ("Broadcast Mode", OSC),
        0x65: ("Snapshot", OSC),
        0x66: ("Still", OSC),
        #67-7F Reserved
        0x80: ("Selection", NAry),
        0x81: ("Assign Selection", OSC),
        0x82: ("Mode Step", OSC),
        0x83: ("Recall Last", OSC),
        0x84: ("Enter Channel", OSC),
        0x85: ("Order Movie", OSC),
        0x86: ("Channel", LC),
        0x87: ("Media Selection", NAry),
        0x88: ("Media Select Computer", Sel),
        0x89: ("Media Select TV", Sel),
        0x8A: ("Media Select WWW", Sel),
        0x8B: ("Media Select DVD", Sel),
        0x8C: ("Media Select Telephone", Sel),
        0x8D: ("Media Select Program Guide", Sel),
        0x8E: ("Media Select Video Phone", Sel),
        0x8F: ("Media Select Games", Sel),
        0x90: ("Media Select Messages", Sel),
        0x91: ("Media Select CD", Sel),
        0x92: ("Media Select VCR", Sel),
        0x93: ("Media Select Tuner", Sel),
        0x94: ("Quit", OSC),
        0x95: ("Help", OOC),
        0x96: ("Media Select Tape", Sel),
        0x97: ("Media Select Cable", Sel),
        0x98: ("Media Select Satellite", Sel),
        0x99: ("Media Select Security", Sel),
        0x9A: ("Media Select Home", Sel),
        0x9B: ("Media Select Call", Sel),
        0x9C: ("Channel Increment", OSC),
        0x9D: ("Channel Decrement", OSC),
        0x9E: ("Media Select SAP", Sel),
        #9F Reserved
        0xA0: ("VCR Plus", OSC),
        0xA1: ("Once", OSC),
        0xA2: ("Daily", OSC),
        0xA3: ("Weekly", OSC),
        0xA4: ("Monthly", OSC),
        #A5-AF Reserved
        0xB0: ("Play", OOC),
        0xB1: ("Pause", OOC),
        0xB2: ("Record", OOC),
        0xB3: ("Fast Forward", OOC),
        0xB4: ("Rewind", OOC),
        0xB5: ("Scan Next Track", OSC),
        0xB6: ("Scan Previous Track", OSC),
        0xB7: ("Stop", OSC),
        0xB8: ("Eject", OSC),
        0xB9: ("Random Play", OOC),
        0xBA: ("Select Disc", NAry),
        0xBB: ("Enter Disc", MC),
        0xBC: ("Repeat", OSC),
        0xBD: ("Tracking", LC),
        0xBE: ("Track Normal", OSC),
        0xBF: ("Slow Tracking", LC),
        0xC0: ("Frame Forward", RTC),
        0xC1: ("Frame Back", RTC),
        0xC2: ("Mark", OSC),
        0xC3: ("Clear Mark", OSC),
        0xC4: ("Repeat From Mark", OOC),
        0xC5: ("Return To Mark", OSC),
        0xC6: ("Search Mark Forward", OSC),
        0xC7: ("Search Mark Backwards", OSC),
        0xC8: ("Counter Reset", OSC),
        0xC9: ("Show Counter", OSC),
        0xCA: ("Tracking Increment", RTC),
        0xCB: ("Tracking Decrement", RTC),
        0xCC: ("Stop/Eject", OSC),
        0xCD: ("Play/Pause", OSC),
        0xCE: ("Play/Skip", OSC),
        #CF-DF Reserved
        0xE0: ("Volume", LC),
        0xE1: ("Balance", LC),
        0xE2: ("Mute", OOC),
        0xE3: ("Bass", LC),
        0xE4: ("Treble", LC),
        0xE5: ("Bass Boost", OOC),
        0xE6: ("Surround Mode", OSC),
        0xE7: ("Loudness", OOC),
        0xE8: ("MPX", OOC),
        0xE9: ("Volume Increment", RTC),
        0xEA: ("Volume Decrement", RTC),
        #EB-EF Reserved
        0xF0: ("Speed Select", OSC),
        0xF1: ("Playback Speed", NAry),
        0xF2: ("Standard Play", Sel),
        0xF3: ("Long Play", Sel),
        0xF4: ("Extended Play", Sel),
        0xF5: ("Slow", OSC),
        #F6-FF Reserved
        0x100: ("Fan Enable", OOC),
        0x101: ("Fan Speed", LC),
        0x102: ("Light Enable", OOC),
        0x103: ("Light Illumination Level", LC),
        0x104: ("Climate Control Enable", OOC),
        0x105: ("Room Temperature", LC),
        0x106: ("Security Enable", OOC),
        0x107: ("Fire Alarm", OSC),
        0x108: ("Police Alarm", OSC),
        0x109: ("Proximity", LC),
        0x10A: ("Motion", OSC),
        0x10B: ("Duress Alarm", OSC),
        0x10C: ("Holdup Alarm", OSC),
        0x10D: ("Medical Alarm", OSC),
        #10E-14F Reserved
        0x150: ("Balance Right", RTC),
        0x151: ("Balance Left", RTC),
        0x152: ("Bass Increment", RTC),
        0x153: ("Bass Decrement", RTC),
        0x154: ("Treble Increment", RTC),
        0x155: ("Treble Decrement", RTC),
        #156-15F Reserved
        0x160: ("Speaker System", CL),
        0x161: ("Channel Left", CL),
        0x162: ("Channel Right", CL),
        0x163: ("Channel Center", CL),
        0x164: ("Channel Front", CL),
        0x165: ("Channel Center Front", CL),
        0x166: ("Channel Side", CL),
        0x167: ("Channel Surround", CL),
        0x168: ("Channel Low Frequency Enhancement", CL),
        0x169: ("Channel Top", CL),
        0x16A: ("Channel Unknown", CL),
        #16B-16F Reserved
        0x170: ("Sub-channel", LC),
        0x171: ("Sub-channel Increment", OSC),
        0x172: ("Sub-channel Decrement", OSC),
        0x173: ("Alternate Audio Increment", OSC),
        0x174: ("Alternate Audio Decrement", OSC),
        #175-17F Reserved
        0x180: ("Application Launch Buttons", NAry),
        0x181: ("AL Launch Button Configuration Tool", Sel),
        0x182: ("AL Programmable Button Configuration", Sel),
        0x183: ("AL Consumer Control Configuration", Sel),
        0x184: ("AL Word Processor", Sel),
        0x185: ("AL Text Editor", Sel),
        0x186: ("AL Spreadsheet", Sel),
        0x187: ("AL Graphics Editor", Sel),
        0x188: ("AL Presentation App", Sel),
        0x189: ("AL Database App", Sel),
        0x18A: ("AL Email Reader", Sel),
        0x18B: ("AL Newsreader", Sel),
        0x18C: ("AL Voicemail", Sel),
        0x18D: ("AL Contacts/Address Book", Sel),
        0x18E: ("AL Calendar/Schedule", Sel),
        0x18F: ("AL Task/Project Manager", Sel),
        0x190: ("AL Log/Journal/Timecard", Sel),
        0x191: ("AL Checkbook/Finance", Sel),
        0x192: ("AL Calculator", Sel),
        0x193: ("AL A/V Capture/Playback", Sel),
        0x194: ("AL Local Machine Browser", Sel),
        0x195: ("AL LAN/WAN Browser", Sel),
        0x196: ("AL Internet Browser", Sel),
        0x197: ("AL Remote Networking/ISP Connect", Sel),
        0x198: ("AL Network Conference", Sel),
        0x199: ("AL Network Chat", Sel),
        0x19A: ("AL Telephony/Dialer", Sel),
        0x19B: ("AL Logon", Sel),
        0x19C: ("AL Logoff", Sel),
        0x19D: ("AL Logon/Logoff", Sel),
        0x19E: ("AL Terminal Lock/Screensaver", Sel),
        0x19F: ("AL Control Panel", Sel),
        0x1A0: ("AL Command Line Processor/Run", Sel),
        0x1A1: ("AL Process/Task Manager", Sel),
        0x1A2: ("AL Select Task/Application", Sel),
        0x1A3: ("AL Next Task/Application", Sel),
        0x1A4: ("AL Previous Task/Application", Sel),
        0x1A5: ("AL Preemptive Halt Task/Application", Sel),
        0x1A6: ("AL Integrated Help Center", Sel),
        0x1A7: ("AL Documents", Sel),
        0x1A8: ("AL Thesaurus", Sel),
        0x1A9: ("AL Dictionary", Sel),
        0x1AA: ("AL Desktop", Sel),
        0x1AB: ("AL Spell Check", Sel),
        0x1AC: ("AL Grammar Check", Sel),
        0x1AD: ("AL Wireless Status", Sel),
        0x1AE: ("AL Keyboard Layout", Sel),
        0x1AF: ("AL Virus Protection", Sel),
        0x1B0: ("AL Encryption", Sel),
        0x1B1: ("AL Screen Saver", Sel),
        0x1B2: ("AL Alarms", Sel),
        0x1B3: ("AL Clock", Sel),
        0x1B4: ("AL File Browser", Sel),
        0x1B5: ("AL Power Status", Sel),
        0x1B6: ("AL Image Browser", Sel),
        0x1B7: ("AL Audio Browser", Sel),
        0x1B8: ("AL Movie Browser", Sel),
        0x1B9: ("AL Digital Rights Manager", Sel),
        0x1BA: ("AL Digital Wallet", Sel),
        #1BB Reserved
        0x1BC: ("AL Instant Messaging", Sel),
        0x1BD: ("AL OEM Features/ Tips/Tutorial Browser", Sel),
        0x1BE: ("AL OEM Help", Sel),
        0x1BF: ("AL Online Community", Sel),
        0x1C0: ("AL Entertainment Content Browser", Sel),
        0x1C1: ("AL Online Shopping Browser", Sel),
        0x1C2: ("AL SmartCard Information/Help", Sel),
        0x1C3: ("AL Market Monitor/Finance Browser", Sel),
        0x1C4: ("AL Customized Corporate News Browser", Sel),
        0x1C5: ("AL Online Activity Browser", Sel),
        0x1C6: ("AL Research/Search Browser", Sel),
        0x1C7: ("AL Audio Player", Sel),
        #1C8-1FF Reserved
        0x200: ("Generic GUI Application Controls", NAry),
        0x201: ("AC New", Sel),
        0x202: ("AC Open", Sel),
        0x203: ("AC Close", Sel),
        0x204: ("AC Exit", Sel),
        0x205: ("AC Maximize", Sel),
        0x206: ("AC Minimize", Sel),
        0x207: ("AC Save", Sel),
        0x208: ("AC Print", Sel),
        0x209: ("AC Properties", Sel),
        0x21A: ("AC Undo", Sel),
        0x21B: ("AC Copy", Sel),
        0x21C: ("AC Cut", Sel),
        0x21D: ("AC Paste", Sel),
        0x21E: ("AC Select All", Sel),
        0x21F: ("AC Find", Sel),
        0x220: ("AC Find and Replace", Sel),
        0x221: ("AC Search", Sel),
        0x222: ("AC Go To", Sel),
        0x223: ("AC Home", Sel),
        0x224: ("AC Back", Sel),
        0x225: ("AC Forward", Sel),
        0x226: ("AC Stop", Sel),
        0x227: ("AC Refresh", Sel),
        0x228: ("AC Previous Link", Sel),
        0x229: ("AC Next Link", Sel),
        0x22A: ("AC Bookmarks", Sel),
        0x22B: ("AC History", Sel),
        0x22C: ("AC Subscriptions", Sel),
        0x22D: ("AC Zoom In", Sel),
        0x22E: ("AC Zoom Out", Sel),
        0x22F: ("AC Zoom", LC),
        0x230: ("AC Full Screen View", Sel),
        0x231: ("AC Normal View", Sel),
        0x232: ("AC View Toggle", Sel),
        0x233: ("AC Scroll Up", Sel),
        0x234: ("AC Scroll Down", Sel),
        0x235: ("AC Scroll", LC),
        0x236: ("AC Pan Left", Sel),
        0x237: ("AC Pan Right", Sel),
        0x238: ("AC Pan", LC),
        0x239: ("AC New Window", Sel),
        0x23A: ("AC Tile Horizontally", Sel),
        0x23B: ("AC Tile Vertically", Sel),
        0x23C: ("AC Format", Sel),
        0x23D: ("AC Edit", Sel),
        0x23E: ("AC Bold", Sel),
        0x23F: ("AC Italics", Sel),
        0x240: ("AC Underline", Sel),
        0x241: ("AC Strikethrough", Sel),
        0x242: ("AC Subscript", Sel),
        0x243: ("AC Superscript", Sel),
        0x244: ("AC All Caps", Sel),
        0x245: ("AC Rotate", Sel),
        0x246: ("AC Resize", Sel),
        0x247: ("AC Flip horizontal", Sel),
        0x248: ("AC Flip Vertical", Sel),
        0x249: ("AC Mirror Horizontal", Sel),
        0x24A: ("AC Mirror Vertical", Sel),
        0x24B: ("AC Font Select", Sel),
        0x24C: ("AC Font Color", Sel),
        0x24D: ("AC Font Size", Sel),
        0x24E: ("AC Justify Left", Sel),
        0x24F: ("AC Justify Center H", Sel),
        0x250: ("AC Justify Right", Sel),
        0x251: ("AC Justify Block H", Sel),
        0x252: ("AC Justify Top", Sel),
        0x253: ("AC Justify Center V", Sel),
        0x254: ("AC Justify Bottom", Sel),
        0x255: ("AC Justify Block V", Sel),
        0x256: ("AC Indent Decrease", Sel),
        0x257: ("AC Indent Increase", Sel),
        0x258: ("AC Numbered List", Sel),
        0x259: ("AC Restart Numbering", Sel),
        0x25A: ("AC Bulleted List", Sel),
        0x25B: ("AC Promote", Sel),
        0x25C: ("AC Demote", Sel),
        0x25D: ("AC Yes", Sel),
        0x25E: ("AC No", Sel),
        0x25F: ("AC Cancel", Sel),
        0x260: ("AC Catalog", Sel),
        0x261: ("AC Buy/Checkout", Sel),
        0x262: ("AC Add to Cart", Sel),
        0x263: ("AC Expand", Sel),
        0x264: ("AC Expand All", Sel),
        0x265: ("AC Collapse", Sel),
        0x266: ("AC Collapse All", Sel),
        0x267: ("AC Print Preview", Sel),
        0x268: ("AC Paste Special", Sel),
        0x269: ("AC Insert Mode", Sel),
        0x26A: ("AC Delete", Sel),
        0x26B: ("AC Lock", Sel),
        0x26C: ("AC Unlock", Sel),
        0x26D: ("AC Protect", Sel),
        0x26E: ("AC Unprotect", Sel),
        0x26F: ("AC Attach Comment", Sel),
        0x270: ("AC Delete Comment", Sel),
        0x271: ("AC View Comment", Sel),
        0x272: ("AC Select Word", Sel),
        0x273: ("AC Select Sentence", Sel),
        0x274: ("AC Select Paragraph", Sel),
        0x275: ("AC Select Column", Sel),
        0x276: ("AC Select Row", Sel),
        0x277: ("AC Select Table", Sel),
        0x278: ("AC Select Object", Sel),
        0x279: ("AC Redo/Repeat", Sel),
        0x27A: ("AC Sort", Sel),
        0x27B: ("AC Sort Ascending", Sel),
        0x27C: ("AC Sort Descending", Sel),
        0x27D: ("AC Filter", Sel),
        0x27E: ("AC Set Clock", Sel),
        0x27F: ("AC View Clock", Sel),
        0x280: ("AC Select Time Zone", Sel),
        0x281: ("AC Edit Time Zones", Sel),
        0x282: ("AC Set Alarm", Sel),
        0x283: ("AC Clear Alarm", Sel),
        0x284: ("AC Snooze Alarm", Sel),
        0x285: ("AC Reset Alarm", Sel),
        0x286: ("AC Synchronize", Sel),
        0x287: ("AC Send/Receive", Sel),
        0x288: ("AC Send To", Sel),
        0x289: ("AC Reply", Sel),
        0x28A: ("AC Reply All", Sel),
        0x28B: ("AC Forward Msg", Sel),
        0x28C: ("AC Send", Sel),
        0x28D: ("AC Attach File", Sel),
        0x28E: ("AC Upload", Sel),
        0x28F: ("AC Download (Save Target As)", Sel),
        0x290: ("AC Set Borders", Sel),
        0x291: ("AC Insert Row", Sel),
        0x292: ("AC Insert Column", Sel),
        0x293: ("AC Insert File", Sel),
        0x294: ("AC Insert Picture", Sel),
        0x295: ("AC Insert Object", Sel),
        0x296: ("AC Insert Symbol", Sel),
        0x297: ("AC Save and Close", Sel),
        0x298: ("AC Rename", Sel),
        0x299: ("AC Merge", Sel),
        0x29A: ("AC Split", Sel),
        0x29B: ("AC Disribute Horizontally", Sel),
        0x29C: ("AC Distribute Vertically", Sel),
        #29D-FFFF Reserved
        },
    #digitizers
    0xd: {
        0x1: ("Digitizer", CA),
        0x2: ("Pen", CA),
        0x3: ("Light Pen", CA),
        0x4: ("Touch Screen", CA),
        0x5: ("Touch Pad", CA),
        0x6: ("White Board", CA),
        0x7: ("Coordinate Measuring Machine", CA),
        0x8: ("3D Digitizer", CA),
        0x9: ("Stereo Plotter", CA),
        0xA: ("Articulated Arm", CA),
        0xB: ("Armature", CA),
        0xC: ("Multiple Point Digitizer", CA),
        0xD: ("Free Space Wand", CA),
        #0E-1F Reserved
        0x20: ("Stylus", CL),
        0x21: ("Puck", CL),
        0x22: ("Finger", CL),
        #23-2F Reserved
        0x30: ("Tip Pressure", DV),
        0x31: ("Barrel Pressure", DV),
        0x32: ("In Range", MC),
        0x33: ("Touch", MC),
        0x34: ("Untouch", OSC),
        0x35: ("Tap", OSC),
        0x36: ("Quality", DV),
        0x37: ("Data Valid", MC),
        0x38: ("Transducer Index", DV),
        0x39: ("Tablet Function Keys", CL),
        0x3A: ("Program Change Keys", CL),
        0x3B: ("Battery Strength", DV),
        0x3C: ("Invert", MC),
        0x3D: ("X Tilt", DV),
        0x3E: ("Y Tilt", DV),
        0x3F: ("Azimuth", DV),
        0x40: ("Altitude", DV),
        0x41: ("Twist", DV),
        0x42: ("Tip Switch", MC),
        0x43: ("Secondary Tip Switch", MC),
        0x44: ("Barrel Switch", MC),
        0x45: ("Eraser", MC),
        0x46: ("Tablet Pick", MC),
        #47-FFFF Reserved
        },
    #0x14 alphanumeric display
    0x14: {
        0x1: ("Alphanumeric Display", CA),
        0x2: ("Bitmapped Display", CA),
        #03-1F Reserved
        0x20: ("Display Attributes Report", CL),
        0x21: ("ASCII Character Set", SF),
        0x22: ("Data Read Back", SF),
        0x23: ("Font Read Back", SF),
        0x24: ("Display Control Report", CL),
        0x25: ("Clear Display", DF),
        0x26: ("Display Enable", DF),
        0x27: ("Screen Saver Delay SV or", DV),
        0x28: ("Screen Saver Enable", DF),
        0x29: ("Vertical Scroll SF or", DF),
        0x2A: ("Horizontal Scroll SF or", DF),
        0x2B: ("Character Report", CL),
        0x2C: ("Display Data", DV),
        0x2D: ("Display Status", CL),
        0x2E: ("Stat Not Ready", Sel),
        0x2F: ("Stat Ready", Sel),
        0x30: ("Err Not a loadable character", Sel),
        0x31: ("Err Font data cannot be read", Sel),
        0x32: ("Cursor Position Report", CL),
        0x33: ("Row", DV),
        0x34: ("Column", DV),
        0x35: ("Rows", SV),
        0x36: ("Columns", SV),
        0x37: ("Cursor Pixel Positioning", SF),
        0x38: ("Cursor Mode", DF),
        0x39: ("Cursor Enable", DF),
        0x3A: ("Cursor Blink", DF),
        0x3B: ("Font Report", CL),
        0x3C: ("Font Data", BufferedBytes),
        0x3D: ("Character Width", SV),
        0x3E: ("Character Height", SV),
        0x3F: ("Character Spacing Horizontal", SV),
        0x40: ("Character Spacing Vertical", SV),
        0x41: ("Unicode Character Set", SF),
        0x42: ("Font 7-Segment", SF),
        0x43: ("7-Segment Direct Map", SF),
        0x44: ("Font 14-Segment", SF),
        0x45: ("14-Segment Direct Map", SF),
        0x46: ("Display Brightness", DV),
        0x47: ("Display Contrast", DV),
        0x48: ("Character Attribute", CL),
        0x49: ("Attribute Readback", SF),
        0x4A: ("Attribute Data", DV),
        0x4B: ("Char Attr Enhance", OOC),
        0x4C: ("Char Attr Underline", OOC),
        0x4D: ("Char Attr Blink", OOC),
        #4E-7F Reserved
        0x80: ("Bitmap Size X", SV),
        0x81: ("Bitmap Size Y", SV),
        #82 Reserved
        0x83: ("Bit Depth Format", SV),
        0x84: ("Display Orientation", DV),
        0x85: ("Palette Report", CL),
        0x86: ("Palette Data Size", SV),
        0x87: ("Palette Data Offset", SV),
        0x88: ("Palette Data", BufferedBytes),
        0x8A: ("Blit Report", CL),
        0x8B: ("Blit Rectangle X1", SV),
        0x8C: ("Blit Rectangle Y1", SV),
        0x8D: ("Blit Rectangle X2", SV),
        0x8E: ("Blit Rectangle Y2", SV),
        0x8F: ("Blit Data", BufferedBytes),
        0x90: ("Soft Button", CL),
        0x91: ("Soft Button ID", SV),
        0x92: ("Soft Button Side", SV),
        0x93: ("Soft Button Offset 1", SV),
        0x94: ("Soft Button Offset 2", SV),
        0x95: ("Soft Button Report", SV),
        #96-FFFF Reserved
    },
    #medical instrument page
    0x40: {
        0x1: ("Medical Ultrasound", CA),
        #02-1F Reserved
        0x20: ("VCR/Acquisition", OOC),
        0x21: ("Freeze/Thaw", OOC),
        0x22: ("Clip Store", OSC),
        0x23: ("Update", OSC),
        0x24: ("Next", OSC),
        0x25: ("Save", OSC),
        0x26: ("Print", OSC),
        0x27: ("Microphone Enable", OSC),
        #28-3F Reserved
        0x40: ("Cine", LC),
        0x41: ("Transmit Power", LC),
        0x42: ("Volume", LC),
        0x43: ("Focus", LC),
        0x44: ("Depth", LC),
        #45-5F Reserved
        0x60: ("Soft Step - Primary", LC),
        0x61: ("Soft Step - Secondary", LC),
        #62-6F Reserved
        0x70: ("Depth Gain Compensation", LC),
        #71-7F Reserved
        0x80: ("Zoom Select", OSC),
        0x81: ("Zoom Adjust", LC),
        0x82: ("Spectral Doppler Mode Select", OSC),
        0x83: ("Spectral Doppler Adjust", LC),
        0x84: ("Color Doppler Mode Select", OSC),
        0x85: ("Color Doppler Adjust", LC),
        0x86: ("Motion Mode Select", OSC),
        0x87: ("Motion Mode Adjust", LC),
        0x88: ("2-D Mode Select", OSC),
        0x89: ("2-D Mode Adjust", LC),
        #8A-9F Reserved
        0xA0: ("Soft Control Select", OSC),
        0xA1: ("Soft Control Adjust", LC),
        #A2-FFFF Reserved
        },
    #
    }
    def __init__(self, pageId, usageId):
        self.pageId = pageId
        self.usageId = usageId
        
    def getButtons(self):
        pass

    def __repr__(self):
        if self.pageId in self.Usages:
            page = self.Usages[self.pageId]
            if self.usageId in page:
                return "%s device, %s usage" % (str(UsagePage(self.pageId)), page[self.usageId][0])
            else:
                return "%s device, Unknown usage" % str(UsagePage(page))
        return "Unknown Page/usage"
        
if __name__ == '__main__':
    #simple testing
    pages = [
        UsagePage(0x8e), #simple
        UsagePage(0x85), #inside range
        UsagePage("Telephony"), #simple
        #UsagePage("Power"), #range
    ]
    for item in pages:
        print item, hex(int(item))
    a = HidUsage(None)
    
