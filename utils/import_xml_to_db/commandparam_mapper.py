
def set_command_param_name(className, paramOrder):
    parameters = {
        "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandSendTksASatz": ["queue", "queue"],
        "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandTksSend": ["stage", "anwIdSender", "blzIdSender", "anwIdEmpfaenger", "blzIdEmpfaenger", "dienstId",
                                                                                  "format", "satzLaenge", "blockLaenge", "alloc", "compress", "convert", "codepage", "Zahlungsformat", "ExterneReferenz"],
        "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandMQPUT": ["queue", "gFormat", "AnwIdSender", "BlzIdSender", "AnwIdEmpfaenger", "BlzIdEmpfaenger", "DienstId", "GFormat", "GCode", "Dateiformat", 
                                                                                "Satzlaenge", "Blocklaenge", "Alloc", "Komprimierung", "Konvertiere", "CodePage", "Zahlungsformat", "DsnMvsInput", "DsnMvsOutput", "ExtReferenz"],
        "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandExecute": ["user", "password", "fingerprints", "soTimeout"],
        "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandChangeDsnOutput": ["rcvaPattern"]
    }

    # Check if className exists
    if className not in parameters:
        raise ValueError(f"Invalid class name: {className}")

    # Check if paramOrder is within range
    if paramOrder < 1 or paramOrder > len(parameters[className]):
        raise IndexError(f"Parameter order {paramOrder} out of range for class {className}")

    # Return the parameter name based on className and paramOrder
    return parameters[className][paramOrder - 1]  # paramOrder is 1-based index
