# Example Notebooks

The example notebooks in this directory demonstrate various functionalities of `HERE Location Services`.

## Prerequisites
Before you run the Notebooks make sure you have:
- A HERE developer account, free and available under [HERE Developer Portal](https://developer.here.com)
- An [API key](https://developer.here.com/documentation/identity-access-management/dev_guide/topics/dev-apikey.html) from the [HERE Developer Portal](https://developer.here.com)

  
## Preparing for visualization

In order to run these Notebooks, you will need a few third-party dependencies. Please copy the following text to a file name anything you like, e.g. `requirements.txt`:

```
jupyterlab
shapely
```

Then run the command `pip install -r requirements.txt`.

For visualization requirements please install [here-map-widget-for-jupyter](https://pypi.org/project/here-map-widget-for-jupyter/).

Follow installation steps from here: [here-map-widget-for-jupyter](https://github.com/heremaps/here-map-widget-for-jupyter#installation).


## Notebooks

- [Location Services](./location_services.ipynb) - Examples of various location services.
- [Restaurant Search](./isoline_routing_restaurant_search.ipynb) - Usecase of restarant search using isoline routing.
- [Routing](./routing.ipynb) - Examples of routing API.
- [Matrix Routing](./matrix_routing.ipynb) - Examples of Matrix routing API.