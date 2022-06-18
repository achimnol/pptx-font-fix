from typing import Final
from pathlib import Path

from lxml import etree

'''
Some sample XML snippets!

# theme/theme1.xml
        <a:fontScheme name="Pretendard">
            <a:majorFont>
                <a:latin typeface="Pretendard"/>
                <a:ea typeface="Pretendard"/>
                <a:cs typeface="Pretendard"/>
                <a:font script="Hang" typeface="Pretendard"/>
            </a:majorFont>
            <a:minorFont>
                <a:latin typeface="Pretendard"/>
                <a:ea typeface="Pretendard"/>
                <a:cs typeface="Pretendard"/>
                <a:font script="Hang" typeface="Pretendard"/>
            </a:minorFont>
        </a:fontScheme>

# presentation.xml
    <p:defaultTextStyle>
        <a:defPPr>
            <a:defRPr lang="ko-Kore-KR"/>
        </a:defPPr>
        <a:lvl1pPr marL="0" algn="l" defTabSz="914400" rtl="0" eaLnBrk="1" latinLnBrk="0" hangingPunct="1">
            <a:defRPr sz="1800" kern="1200">
                <a:solidFill>
                    <a:schemeClr val="tx1"/>
                </a:solidFill>
                <a:latin typeface="+mn-lt"/>
                <a:ea typeface="+mn-ea"/>
                <a:cs typeface="+mn-cs"/>
            </a:defRPr>
        </a:lvl1pPr>
        ...
    </p:defaultTextStyle>

# slideMasters/slideMaster1.xml
        <p:titleStyle>
            <a:lvl1pPr algn="l" defTabSz="914400" rtl="0" eaLnBrk="1" latinLnBrk="0" hangingPunct="1">
                <a:lnSpc>
                    <a:spcPct val="90000"/>
                </a:lnSpc>
                <a:spcBef>
                    <a:spcPct val="0"/>
                </a:spcBef>
                <a:buNone/>
                <a:defRPr sz="4400" b="1" kern="1200">
                    <a:solidFill>
                        <a:schemeClr val="tx1"/>
                    </a:solidFill>
                    <a:latin typeface="+mj-lt"/>
                    <a:ea typeface="+mj-ea"/>
                    <a:cs typeface="+mj-cs"/>
                </a:defRPr>
            </a:lvl1pPr>
        </p:titleStyle>
        <p:bodyStyle>
            <a:lvl1pPr marL="228600" indent="-228600" algn="l" defTabSz="914400" rtl="0" eaLnBrk="1" latinLnBrk="0" hangingPunct="1">
                <a:lnSpc>
                    <a:spcPct val="90000"/>
                </a:lnSpc>
                <a:spcBef>
                    <a:spcPts val="1000"/>
                </a:spcBef>
                <a:buFont typeface="Arial" panose="020B0604020202020204" pitchFamily="34" charset="0"/>
                <a:buChar char="•"/>
                <a:defRPr sz="2800" kern="1200">
                    <a:solidFill>
                        <a:schemeClr val="tx1"/>
                    </a:solidFill>
                    <a:latin typeface="+mn-lt"/>
                    <a:ea typeface="+mn-ea"/>
                    <a:cs typeface="+mn-cs"/>
                </a:defRPr>
            </a:lvl1pPr>
            ...
        </p:bodyStyle>

# slideLayouts/slideLayout1.xml
        (TODO)


# slides/slide1.xml
# slides/slide2.xml
# slides/slide3.xml
'''

xmlns: Final = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}


def local_tag(tag_name) -> str:
    """Strip out the namespace from the element tag name."""
    return etree.QName(tag_name).localname


def _print_font_scheme(font_scheme: etree.Element, indent: str = "") -> None:
    for font_elem in font_scheme.getchildren():
        print(f"{indent}{local_tag(font_elem.tag)}:")
        for prev_typeface in font_elem.getchildren():
            prev_script_name = local_tag(prev_typeface.tag)
            match prev_script_name:
                case "font":
                    print(
                        f"{indent}  "
                        f"{prev_script_name} ({prev_typeface.get('script')}): "
                        f"{prev_typeface.get('typeface')}"
                    )
                case _:
                    print(
                        f"{indent}  "
                        f"{prev_script_name}: {prev_typeface.get('typeface')}"
                    )

def fix_theme_font(
    work_path: Path,
    major_font: str,
    minor_font: str,
) -> None:
    theme_dir = work_path / 'ppt' / 'theme'
    for theme_path in theme_dir.glob('theme*.xml'):
        root_elem = etree.parse(theme_path)
        font_scheme_elem = root_elem.xpath('//a:fontScheme', namespaces=xmlns)[0]

        # Print out current theme font configuration
        print(f"Current font scheme: (name={font_scheme_elem.get('name')!r})")
        _print_font_scheme(font_scheme_elem, indent="  ")

        # Replace the theme font
        major_font_elem = etree.Element(etree.QName(xmlns['a'], 'majorFont'))
        major_font_elem.append(etree.Element(etree.QName(xmlns['a'], 'latin'), attrib={'typeface': major_font}))
        major_font_elem.append(etree.Element(etree.QName(xmlns['a'], 'ea'), attrib={'typeface': major_font}))
        major_font_elem.append(etree.Element(etree.QName(xmlns['a'], 'cs'), attrib={'typeface': major_font}))
        major_font_elem.append(etree.Element(etree.QName(xmlns['a'], 'sym'), attrib={'typeface': major_font}))
        major_font_elem.append(etree.Element(etree.QName(xmlns['a'], 'font'), attrib={'script': 'Hang', 'typeface': major_font}))
        minor_font_elem = etree.Element(etree.QName(xmlns['a'], 'minorFont'))
        minor_font_elem.append(etree.Element(etree.QName(xmlns['a'], 'latin'), attrib={'typeface': minor_font}))
        minor_font_elem.append(etree.Element(etree.QName(xmlns['a'], 'ea'), attrib={'typeface': minor_font}))
        minor_font_elem.append(etree.Element(etree.QName(xmlns['a'], 'cs'), attrib={'typeface': minor_font}))
        minor_font_elem.append(etree.Element(etree.QName(xmlns['a'], 'sym'), attrib={'typeface': minor_font}))
        minor_font_elem.append(etree.Element(etree.QName(xmlns['a'], 'font'), attrib={'script': 'Hang', 'typeface': minor_font}))
        font_scheme_attrib = {**font_scheme_elem.attrib}
        font_scheme_elem.clear()
        for k, v in font_scheme_attrib.items():
            font_scheme_elem.set(k, v)
        font_scheme_elem.append(major_font_elem)
        font_scheme_elem.append(minor_font_elem)

        print(f"New font scheme: (name={font_scheme_elem.get('name')!r})")
        _print_font_scheme(font_scheme_elem, indent="  ")

        # Write back
        root_elem.write(theme_path)


def normalize_master_fonts(
    work_path: Path,
    bullet_font: str = "+mn-lt",
    *,
    major_bold: bool = True,
    minor_bold: bool = False,
) -> None:
    # TODO: presentation.xml: change defRPr typefaces in defaultTextStyle
    # TODO: slideMasterN.xml: change buFont typeface
    # TODO: slideMasterN.xml: change defRPr typefaces in titleStyle and bodyStyle
    pass


def normalize_slide_fonts(work_path: Path) -> None:
    # TODO: ...
    pass
