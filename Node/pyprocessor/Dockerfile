# Copyright 2018 Intel Corporation
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
# -----------------------------------------------------------------------------

FROM test
EXPOSE 4004/tcp
RUN echo fc747a11f43f7686c78b07f784cc3ffdb712ef79d8beb119adf42e90cc4c2664 > priv.txt
COPY / .
ENV PATH "$PATH:/project/simplewallet/pyprocessor"

CMD bash -c './simplewallet-tp'

