"""Utility classes for Jupyter notebook integration."""


class HtmlFormatter:
    """A mixin class to provide HTML representation for Jupyter notebooks."""

    def _repr_html_(self, content=None, with_header=True):
        """HTML representation for Jupyter notebooks.

        Parameters
        ----------
        content : str, optional
            The main content to display in HTML format. Defaults to None.
        with_header : bool, optional
            Whether to include a header with the class name. Defaults to True.

        Returns
        -------
        str
            The HTML representation.
        """
        html = """
            <style type="text/css">
                div.pydov {
                    background-color: rgba(170,170,170,0.05);
                    padding: 10px;
                    padding-left: 20px;
                    border-left: 1px solid #fee439;
                    border-radius: 10px;
                    margin: 10px 0;
                    max-height: 50vh;
                    overflow: auto;
                }

                .code {
                    font-family: monospace;
                }

                .small {
                    font-size: 0.8rem;
                }
            </style>
            <div class="pydov">
        """

        if with_header:
            html += f"""
                <div class="classname code">
                    {self.__class__.__module__ + '.' + self.__class__.__name__}
                </div>
            """

        if content is not None:
            html += content

        html += """
            </div>
        """
        return html
