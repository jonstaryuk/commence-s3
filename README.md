# commence-s3

A script for quickly creating a new static site on S3.

It makes a new bucket, adds a bucket policy granting public read access, configures the static website with `index.html` and `error.html` pages, and opens it in your browser.

Usage:

```
$ python commence.py your.project.site.com
```
