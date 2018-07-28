# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""Setup script for log uniform sampler"""
from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy

extension_name = 'log_uniform'
sources = ['log_uniform.pyx', 'LogUniformGenerator.cc']
setup(ext_modules=cythonize(Extension(extension_name,
                                      sources=sources,
                                      language='c++',
                                      extra_compile_args=['-std=c++11'],
                                      include_dirs=[numpy.get_include()])))
