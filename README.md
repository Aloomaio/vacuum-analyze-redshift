
# Usage

You need to install [Docker](https://www.docker.com/get-docker) on your machine.

Please refer to our [blog post][alooma-blog-post] for a detailed explanation.

# Development

The Vacuum and Analyze logic is built by [awslabs/amazon-redshift-utils][1]. If you find a bug or would like to suggest a feature, please create a pull request over there.

The Docker wrapper and the entrypoint is built by us. If you would like to fix a bug or a suggest a feature, please create a pull request in this repository.

# License

* The provided Dockerfile using a script developed by [`amazon-redshift-utils`][amazon-redshift-utils-license]. 

* Our project is released under the [Apache 2.0 License][apache-2-license].


* Note that the upstream tool [`amazon-redshift-utils`][amazon-redshift-utils-license] is released under the [Amazon Software License][asl].



[amazon-redshift-utils-license]: https://github.com/awslabs/amazon-redshift-utils/blob/master/LICENSE.txt
[apache-2-license]: https://choosealicense.com/licenses/apache-2.0/
[asl]: http://aws.amazon.com/asl/
[alooma-blog-post]: https://www.alooma.com
[1]: https://github.com/awslabs/amazon-redshift-utils.git
