Prerequisites
=============
Before you can install `HERE Location Services for Python`, run its test-suite, or use the example notebooks to make sure you meet the following prerequisites:

* A Python installation, 3.6+ recommended, with the `pip` command available to install dependencies.

* In order to use Location services APIs, authentication is required.

  There are two ways to authenticate:
  * Authentication using an API key:

    * For API key-based authentication you will need a HERE developer account, freely available under `HERE Developer Portal`_.
    * An `API key`_ from the `HERE Developer Portal`_, in an environment variable named `LS_API_KEY` which you can set like this (with a valid value, of course)::

      $ export LS_API_KEY="MY-LS-API-KEY"

  * OAuth token-based authentication:

    * For OAuth token authentication you will need an account on the HERE Platform.
      To get more details on the HERE Platform account please check our documentation `Get a HERE account <https://developer.here.com/documentation/identity-access-management/dev_guide/topics/obtain-user-credentials.html>`_.

    Once you have the account follow the below steps to get credentials:

    * Go to `HERE Platform Applications and Keys <https://platform.here.com/profile/apps-and-keys>`_ and register a new app.

    * Create a key for the app and download the generated ` credentials. properties` file.

    The HERE platform generated app credentials should look similar to the example below::

        here.user.id = <example_here>
        here.client.id = <example_here>
        here.access.key.id = <example_here>
        here.access.key.secret = <example_here>
        here.token.endpoint.url = <example_here>

    You can provide your credentials using any of the following methods:

    * Default credentials

    Place the credentials file into

    For Linux/MacOS: `$HOME/.here/credentials.properties`

    For Windows: `%USERPROFILE%\.here\credentials.properties`
    Code snippet to instantiate LS object::

        from here_location_services import LS

        # platform credentials will be picked from the default credentials file's location mentioned above
        # and api_key should not be set in env variable LS_API_KEY.
        ls = LS()

    * Environment Variables

    You can override default credentials by assigning values to the following environment variables::

        HERE_USER_ID
        HERE_CLIENT_ID
        HERE_ACCESS_KEY_ID
        HERE_ACCESS_KEY_SECRET
        HERE_TOKEN_ENDPOINT_URL

    Code snippet to instantiate LS object::

        from here_location_services import LS
        from here_location_services import PlatformCredentials

        ls = LS(platform_credentials=PlatformCredentials.from_env())

    * Credentials File

    You can specify any credentials file as an alternative to that found in `~/.here/credentials.properties`. An error is generated if there is no file present at the path, or if the file is not properly formatted.
    Code snippet to instantiate LS object::

        from here_location_services import LS
        from here_location_services import PlatformCredentials

        platform_credentials = PlatformCredentials.from_credentials_file("<Path_to_file>")
        ls = LS(platform_credentials=platform_credentials)

.. _HERE Developer Portal: https://developer.here.com/
.. _API key: https://developer.here.com/documentation/identity-access-management/dev_guide/topics/dev-apikey.html