# Copyright 2012-2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import yaml
from yaml.resolver import ScalarNode, SequenceNode


def intrinsics_multi_constructor(loader, tag_prefix, node):
    """
    YAML constructor to parse CloudFormation intrinsics.
    This will return a dictionary with key being the instrinsic name
    """

    # Get the actual tag name excluding the first exclamation
    tag = node.tag[1:]

    # All CloudFormation intrinsics have prefix Fn:: except Ref
    prefix = "Fn::"
    if tag == "Ref":
        prefix = ""

    cfntag = prefix + tag

    if tag == "GetAtt":
        # ShortHand notation for !GetAtt accepts Resource.Attribute format
        # while the standard notation is to use an array
        # [Resource, Attribute]. Convert shorthand to standard format
        value = node.value.split(".", 1)

    elif isinstance(node, ScalarNode):
        # Value of this node is scalar
        value = loader.construct_scalar(node)

    elif isinstance(node, SequenceNode):
        # Value of this node is an array (Ex: [1,2])
        value = loader.construct_sequence(node)

    else:
        # Value of this node is an mapping (ex: {foo: bar})
        value = loader.construct_mapping(node)

    return {cfntag: value}


def yaml_dump(dict_to_dump):
    """
    Dumps the dictionary as a YAML document
    :param dict_to_dump:
    :return:
    """
    return yaml.safe_dump(dict_to_dump, default_flow_style=False)


def yaml_parse(yamlstr):

    yaml.SafeLoader.add_multi_constructor("!", intrinsics_multi_constructor)

    return yaml.safe_load(yamlstr)
