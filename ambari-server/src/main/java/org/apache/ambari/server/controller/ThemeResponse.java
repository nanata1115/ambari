/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 * <p>
 * http://www.apache.org/licenses/LICENSE-2.0
 * <p>
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.apache.ambari.server.controller;


import org.apache.ambari.server.state.theme.Theme;

import io.swagger.annotations.ApiModelProperty;

/**
 * Response schema for endpoint {@link org.apache.ambari.server.api.services.StacksService#getStackService(String,
 *                              jakarta.ws.rs.core.HttpHeaders, jakarta.ws.rs.core.UriInfo, String, String, String)}
 */
public interface ThemeResponse extends ApiModel {

  @ApiModelProperty(name = "ThemeInfo")
  ThemeInfoResponse getThemeInfo();


  interface ThemeInfoResponse {
    @ApiModelProperty(name = "default")
    boolean isDefault();

    @ApiModelProperty(name = "file_name")
    String getFileName();

    @ApiModelProperty(name = "service_name")
    String getServiceName();

    @ApiModelProperty(name = "stack_name")
    String getStackName();

    @ApiModelProperty(name = "stack_version")
    String getStackVersion();

    @ApiModelProperty(name = "theme_data")
    Theme getThemeData();
  }

}
