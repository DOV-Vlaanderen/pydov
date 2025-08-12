class HtmlFormatter:
    def _repr_html_(self, content=None, with_header=True):
        html = """
            <style type="text/css">
                div.pydov {
                    background-color: rgba(128,128,128,0.05);
                    padding: 10px;
                    padding-left: 20px;
                    border-left: 1px solid #fee439;
                    border-radius: 10px;
                    margin: 10px 0;
                }

                .code {
                    font-family: monospace;
                }

                .methods {
                    margin-left: 10px;
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
