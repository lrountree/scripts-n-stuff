# Logging script, import to existing scripts for compact code
# Lucas Rountree 2020
#

# Import common modules
import sys
import logging

# Logging function or class
class LOG:
    """ -- Usage --
    log.LOG('Logger', 'Destionation_File_Path', 'Console_Level', 'File_Level').[level]('Log_Data')
    Command Line: 
        log.py 'Logger' 'Destination_File_Path' 'Console_Level' 'File_Level' '[level]' 'Log_Data'
    As Module:
        from log import LOG
        log = LOG('Logger = ', 'Destination_File_Path = ', 'Console_Level = ', 'File_Level = ')
        log.<level>('Log_Data')
    -- Definitions --
    Logger - custom name for the logger, for easier identification
    Destination_File_Path - where to write log data, requires full path to file on disk
    Console_Level - set level of log detail to stream to the console
    File_Level - set level of log detail to stream to file
    [level] - set current level of log detail
    Log_Data - data to log
    -- Defaults --
    Logger - python_logger
    Destination_File_Path - False (do not write to a file)
    Console_Level - debug
    File_Level - debug
    -- Required Input --
    Log_Data
    -- Level Options --
    debug, info, warning, error, critical
    """
    
    def __init__(self, Logger = 'python_logger', Destination_File_Path = False, Console_Level = 'debug', File_Level = 'debug'):
        global logger
        logger = logging.getLogger(Logger) # Create logger
        logger.setLevel(logging.DEBUG) # Set base log detail level
        Console_Handler = logging.StreamHandler() # Create console handler to stream to console
        if Console_Level == 'debug': # Check and set level of log detail for the console stream
            Console_Handler.setLevel(logging.DEBUG)
        elif Console_Level == 'info':
            Console_Handler.setLevel(logging.INFO)
        elif Console_Level == 'warning':
            Console_Handler.setLevel(logging.WARNING)
        elif Console_Level == 'error':
            Console_Handler.setLevel(logging.ERROR)
        elif Console_Level == 'critical':
            Console_Handler.setLevel(logging.CRITICAL)
        Console_Handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s')) # Format console stream
        logger.addHandler(Console_Handler)
        if Destination_File_Path: # Check if log file is specified, do not use if not specified
            File_Handler = logging.FileHandler(Destination_File_Path) # Create file handler to stream to a file
            if File_Level == 'debug': # Check and set level of log detail for the file stream
                File_Handler.setLevel(logging.DEBUG)
            elif File_Level == 'info':
                File_Handler.setLevel(logging.INFO)
            elif File_Level == 'warning':
                File_Handler.setLevel(logging.WARNING)
            elif File_Level == 'error':
                File_Handler.setLevel(logging.ERROR)
            elif File_Level == 'critical':
                File_Handler.setLevel(logging.CRITICAL)
            File_Handler.setFormatter(logging.Formatter('%(asctime)s %(name)s.%(levelname)s: %(message)s')) # Format file stream
        else:
            File_Handler = logging.NullHandler() # Dump to null
        logger.addHandler(File_Handler)

    # Set up logging functions as part of the LOG class
    def debug(self, Log_Data):
        """debug level logging
        """
        logger.debug(Log_Data)
    def info(self, Log_Data):
        """info level logging
        """
        logger.info(Log_Data)
    def warning(self, Log_Data):
        """warning level logging
        """
        logger.warning(Log_Data)
    def error(self, Log_Data):
        """error level logging
        """
        logger.error(Log_Data)
    def critical(self, Log_Data):
        """critical level logging
        """
        logger.critical(Log_Data)

# Run as a script
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Log data and config options.', prog='log')
    parser.add_argument('-n', action='store', default='', help='Name the logger, default: python_logger')
    parser.add_argument('-d', action='store', default='', help='Destination log file, default: do not log to file')
    parser.add_argument('-c', choices=['debug', 'info', 'warning', 'error', 'critical'], action='store', default='', help='Level to stream log to the console, default: debug')
    parser.add_argument('-f', choices=['debug', 'info', 'warning', 'error', 'critical'], action='store', default='', help='Level to stream log to the destination log file, default: debug')
    parser.add_argument('-l', required=True, choices=['debug', 'info', 'warning', 'error', 'critical'], action='store', help='Set log level *required*')
    parser.add_argument('-i', required=True, action='store', type=str, help='Log data input *required*')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0', help='Current version of log.py')
    args = parser.parse_args()

    Level_Function = args.l
    log = LOG(args.n, args.d, args.c, args.f)

    if args.l == 'debug':
        log.debug(args.i)
    elif args.l == 'info':
        log.info(args.i)
    elif args.l == 'warning':
        log.warning(args.i)
    elif args.l == 'error':
        log.error(args.i)
    elif args.l == 'critical':
        log.critical(args.i)
