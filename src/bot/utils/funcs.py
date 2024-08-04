#
# (c) 2024, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from re import search


def extract_number_from_command(command: str):
    match = search(r'/start (\d+)', command)
    if match:
        return int(match.group(1))
    return None


def extract_number_from_text_by_prefix(prefix: str, text: str):
    match = search(rf'{prefix}:(\d+)', text)
    if match:
        return int(match.group(1))
    return None
