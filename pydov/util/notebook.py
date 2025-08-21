
class AbstractDictLike:
    def __init__(self, base_dict=dict()):
        self.base_dict = base_dict

    def __dir__(self):
        return list(self.base_dict.keys())

    def __contains__(self, name):
        return name in self.base_dict

    def __iter__(self):
        return self.base_dict.__iter__()

    def __getitem__(self, name):
        if name in self.base_dict:
            return self.base_dict.get(name)
        raise KeyError(f'{name}')

    def __getattr__(self, name):
        if name in self.base_dict:
            return self.base_dict.get(name)
        raise AttributeError(
            f"'{self.__class__.__name__}' object has not attribute '{name}'")

    def __repr__(self):
        return self.base_dict.__repr__()

    def keys(self):
        return self.base_dict.keys()

    def values(self):
        return self.base_dict.values()


class HtmlFormatter:
    def _repr_html_(self, content=None, with_header=True):
        html = """
            <style type="text/css">
                div.pydov {
                    background-color: rgba(170,170,170,0.05);
                    padding: 10px;
                    padding-left: 20px;
                    border-left: 1px solid #fee439;
                    border-radius: 10px;
                    margin: 10px 0;
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
