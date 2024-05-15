#!/usr/bin/env python3

"""
Module: expiring_web_cache

This module provides functionality to cache web pages with
an expiration time using Redis.

Functions:
    wrap_requests(fn):
        A decorator to wrap a function and cache its results
        with an expiration time.
    get_page(url):
        Fetch a web page and return its content, using caching
        to store the result.

"""

import redis
import requests
from typing import Callable
from functools import wraps

# Initialize a Redis client
redis_client = redis.Redis()


def wrap_requests(fn: Callable) -> Callable:
    """
    Decorator to wrap a function and cache its results
    with an expiration time.

    Args:
        fn (Callable): The function to be decorated.

    Returns:
        Callable: The wrapped function.
    """
    @wraps(fn)
    def wrapper(url):
        """
        Wrapper function to manage caching.

        Args:
            url (str): The URL to fetch.

        Returns:
            str: The content of the web page.
        """
        # Increment the count of URL accesses
        redis_client.incr(f"count:{url}")

        # Check if the response is cached
        cached_response = redis_client.get(f"cached:{url}")
        if cached_response:
            return cached_response.decode('utf-8')

        # Fetch the result and cache it with an expiration time of 10 seconds
        result = fn(url)
        redis_client.setex(f"cached:{url}", 10, result)
        return result

    return wrapper


@wrap_requests
def get_page(url: str) -> str:
    """
    Fetch a web page and return its content.

    Args:
        url (str): The URL of the web page to fetch.

    Returns:
        str: The content of the web page.
    """
    response = requests.get(url)
    return response.text
