command_params = {
    "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandSendTksASatz": ["queue1", "queue2"],
    "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandTksSend": ["stage", "anwIdSender", "blzIdSender", "anwIdEmpfaenger", "blzIdEmpfaenger", "dienstId",
                                                                                  "format", "satzLaenge", "blockLaenge", "alloc", "compress", "convert", "codepage", "Zahlungsformat", "ExterneReferenz"],
    "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandMQPUT": ["queue", "gFormat", "AnwIdSender", "BlzIdSender", "AnwIdEmpfaenger", "BlzIdEmpfaenger", "DienstId", "GFormat", "GCode", "Dateiformat", 
                                                                                "Satzlaenge", "Blocklaenge", "Alloc", "Komprimierung", "Konvertiere", "CodePage", "Zahlungsformat", "DsnMvsInput", "DsnMvsOutput", "ExtReferenz"],
    "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandExecute": ["user", "password", "fingerprints", "soTimeout"],
    "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandChangeDsnOutput": ["rcvaPattern"]
}

def set_command_param_name(className, paramOrder):

    if className not in command_params:
        raise ValueError(f"Invalid class name: {className}")

    if paramOrder < 1 or paramOrder > len(command_params[className]):
        raise IndexError(f"Parameter order {paramOrder} out of range for class {className}")

    return command_params[className][paramOrder - 1]
