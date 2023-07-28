from typing import Optional
import re
import pylinks


class DOI:
    """

    References
    ----------
    https://citation.crosscite.org/docs.html
    https://www.doi.org/hb.html
    https://support.datacite.org/docs/doi-basics
    """

    def __init__(self, doi: str):
        """
        Parameters
        ----------
        doi : str
            Digital Object Identifier (DOI) of a publication,
            either as a URL (optionally starting with either 'http://' or 'https://',
            followed by either 'dx.doi.org/' or 'doi.org/', and then the identifier),
            or the identifier alone (starting with '10.'). For example:
            * '10.3762/bjoc.17.8'
            * 'https://doi.org/10.1039/d2sc03130b'
            * 'dx.doi.org/10.1093/nar/gkac267'
        """
        match = re.match(r'(?:https?://)?(?:dx\.)?(?:doi\.org/)?(10\.\d+/\S+)', doi)
        if not match:
            raise ValueError(f"Invalid DOI: {doi}")
        self.doi = match.group(1)
        self.url = f"https://doi.org/{self.doi}"  # See also: https://api.crossref.org/works/{doi}
        return

    def text(self, style: Optional[str] = None, locale: Optional[str] = None) -> str:
        """
        Formatted text citation for the DOI, with an optional citation style and locale.

        The citation is generated by the [Citation Style Language](https://citationstyles.org/)
        (CSL) processor (citeproc).

        Parameters
        ----------
        style : str, optional
            Citation style, e.g. APA, Harvard, Angewandte Chemie etc.
            More than 1000 styles are available; see https://github.com/citation-style-language/styles.
        locale : str, optional
            Locale to use for the citation; see https://github.com/citation-style-language/locales.
        """
        accept = 'text/x-bibliography'
        if style:
            accept += f'; style={style}'
        if locale:
            accept += f'; locale={locale}'
        return pylinks.request(
            self.url,
            headers={"accept": accept},
            encoding="utf-8",
            response_type='str'
        )

    @property
    def bibtex(self) -> str:
        return pylinks.request(
            self.url,
            headers={"accept": "application/x-bibtex"},
            encoding="utf-8",
            response_type='str'
        )

    @property
    def ris(self) -> str:
        return pylinks.request(
            self.url,
            headers={"accept": "application/x-research-info-systems"},
            encoding="utf-8",
            response_type='str'
        )

    @property
    def citeproc_dict(self) -> dict:
        """
        Citation data as a dictionary with Citeproc JSON schema.
        """
        return pylinks.request(
            self.url,
            headers={"accept": "application/citeproc+json"},
            encoding="utf-8",
            response_type='json'
        )


def doi(doi: str) -> DOI:
    return DOI(doi=doi)
