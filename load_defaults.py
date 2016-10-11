""" Parse defaults from a config file """
from configparser import SafeConfigParser, NoSectionError
from os.path import dirname, exists, join, realpath


def load_config_file(conf_file, section, defaults):
    """Load the configuration file.

    :param str conf_file: The configuration file
    :param str section: The name of the section to read
    :param dict defaults: The defaults value of the arguments
    :rtype: :py:class:`dict`
    :return: The defaults value of the arguments using the values from the
        configuration file

    """
    if conf_file:
        config = SafeConfigParser(allow_no_value=True)
        config.read(conf_file)

        try:
            defaults.update(dict(config.items(section)))
        except NoSectionError as error:
            missing = ("File {file} (or section {section} in {file}) missing"
                       .format(file=realpath(conf_file), section=section))
            print("! {missing}".format(missing=missing))
            print(error)
            exit(0)

        print("Read {section} from {file}"
              .format(file=realpath(conf_file), section=section))

    return defaults
