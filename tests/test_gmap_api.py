def test_api_return_none():
    return {"candidates" : [],
            "status" : "ZERO_RESULTS"}

def test_api_return_one():
    results = {
                "candidates" : [
                    {
                        "formatted_address" : "Place d'Armes, 78000 Versailles, France",
                        "geometry" : {
                            "location" : {
                            "lat" : 48.8048649,
                            "lng" : 2.1203554
                            },
                            "viewport" : {
                            "northeast" : {
                                "lat" : 48.80568935,
                                "lng" : 2.1253615
                            },
                            "southwest" : {
                                "lat" : 48.80239155,
                                "lng" : 2.1186867
                            }
                            }
                        },
                        "name" : "Château de Versailles"
                    }
                ],
                "status" : "OK"
                }
    return results


def test_api_return_multiple():
    results = {
            "candidates" : [
                {
                    "formatted_address" : "22940 Saint-Julien, France",
                    "geometry" : {
                        "location" : {
                        "lat" : 48.453224,
                        "lng" : -2.814378
                        },
                        "viewport" : {
                        "northeast" : {
                            "lat" : 48.460788,
                            "lng" : -2.793771
                        },
                        "southwest" : {
                            "lat" : 48.4364341,
                            "lng" : -2.8416309
                        }
                        }
                    },
                    "name" : "Saint-Julien"
                },
                {
                    "formatted_address" : "69640 Saint-Julien, France",
                    "geometry" : {
                        "location" : {
                        "lat" : 46.02602599999999,
                        "lng" : 4.653080999999999
                        },
                        "viewport" : {
                        "northeast" : {
                            "lat" : 46.036325,
                            "lng" : 4.683454
                        },
                        "southwest" : {
                            "lat" : 46.014078,
                            "lng" : 4.612508099999999
                        }
                        }
                    },
                    "name" : "Saint-Julien"
                },
                {
                    "formatted_address" : "74160 Saint-Julien-en-Genevois, France",
                    "geometry" : {
                        "location" : {
                        "lat" : 46.144516,
                        "lng" : 6.081338
                        },
                        "viewport" : {
                        "northeast" : {
                            "lat" : 46.1519901,
                            "lng" : 6.128467
                        },
                        "southwest" : {
                            "lat" : 46.12289089999999,
                            "lng" : 6.046807299999999
                        }
                        }
                    },
                    "name" : "Saint-Julien-en-Genevois"
                }
            ],
            "status" : "OK"
            }
    return results