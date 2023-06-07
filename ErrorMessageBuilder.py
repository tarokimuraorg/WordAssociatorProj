def message(file_name : str, function_name : str, error_type : str, error_message : str) -> str:

    message = '\n'
    message += '   error type : {}\n'.format(error_type)
    message += 'error message : {}\n'.format(error_message)
    message += '    file name : {}\n'.format(file_name)
    message += 'function name : {}\n'.format(function_name)

    return message
