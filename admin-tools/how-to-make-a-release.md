<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Get latest sources:](#get-latest-sources)
- [Change version in trepan/version.py:](#change-version-in-trepanversionpy)
- [Update ChangeLog:](#update-changelog)
- [Update NEWS from ChangeLog:](#update-news-from-changelog)
- [Make sure pyenv is running and check newer versions](#make-sure-pyenv-is-running-and-check-newer-versions)
- [Switch to python-2.4, sync that up and build that first since it creates a tarball which we don't want.](#switch-to-python-24-sync-that-up-and-build-that-first-since-it-creates-a-tarball-which-we-dont-want)
- [Check against older versions](#check-against-older-versions)
- [Make packages and tag](#make-packages-and-tag)
- [Upload](#upload)
- [Push tags:](#push-tags)

<!-- markdown-toc end -->
# Get latest sources:

    $ git pull

# Change version in trepan/version.py:

	$ emacs trepan/version.py
    $ source trepan/version.py
    $ echo $VERSION
    $ git commit -m"Get ready for release $VERSION" .

# Update ChangeLog:

    $ make ChangeLog

#  Update NEWS from ChangeLog:

    $ make check-short
    $ git commit --amend .
    $ git push # get CI testing going early

# Make sure pyenv is running and check newer versions

    $ pyenv local && source admin-tools/check-newer-versions.sh


# Switch to python-2.4, sync that up and build that first since it creates a tarball which we don't want.

    $ source admin-tools/setup-python-2.4.sh

    $ git merge master
	# Add and fix merge conflicts
	$ git commit

# Check against older versions

    $ source admin-tools/check-older-versions.sh

# Make packages and tag

    $ . ./admin-tools/make-dist-older.sh
	$ pyenv local 3.8.3
	$ twine check dist/trepan2-$VERSION*
    $ git tag release-python-2.4-$VERSION
    $ . ./admin-tools/make-dist-newer.sh
	$ twine check dist/trepan2-$VERSION*


# Upload

    $ twine upload dist/trepan2-${VERSION}*

# Push tags:

    $ git push --tags
