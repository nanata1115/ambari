/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.ambari.server.api.services;

import java.util.HashMap;
import java.util.Map;

import jakarta.ws.rs.DELETE;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.PUT;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.PathParam;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.Context;
import jakarta.ws.rs.core.HttpHeaders;
import jakarta.ws.rs.core.Response;
import jakarta.ws.rs.core.UriInfo;

import io.swagger.v3.oas.annotations.Hidden;
import org.apache.ambari.server.api.resources.ResourceInstance;
import org.apache.ambari.server.controller.spi.Resource;

/**
 * WidgetLayout Service
 */
public class WidgetLayoutService extends BaseService {
  
  private final String clusterName;

  public  WidgetLayoutService(String clusterName) {
    this.clusterName = clusterName;
  }

  @GET @Hidden // until documented
  @Path("{widgetLayoutId}")
  @Produces("text/plain")
  public Response getService(String body, @Context HttpHeaders headers, @Context UriInfo ui,
                             @PathParam("widgetLayoutId") String widgetLayoutId) {

    return handleRequest(headers, body, ui, Request.Type.GET,
            createResource(widgetLayoutId));
  }

  /**
   * Handles URL: /widget_layouts
   * Get all instances for a view.
   *
   * @param headers  http headers
   * @param ui       uri info
   *
   * @return instance collection resource representation
   */
  @GET @Hidden // until documented
  @Produces("text/plain")
  public Response getServices(String body, @Context HttpHeaders headers, @Context UriInfo ui) {
    return handleRequest(headers, body, ui, Request.Type.GET,
            createResource(null));
  }

  @POST @Hidden // until documented
  @Path("{widgetLayoutId}")
  @Produces("text/plain")
  public Response createService(String body, @Context HttpHeaders headers, @Context UriInfo ui,
                                @PathParam("widgetLayoutId") String widgetLayoutId) {
    return handleRequest(headers, body, ui, Request.Type.POST,
            createResource(widgetLayoutId));
  }

  @POST @Hidden // until documented
  @Produces("text/plain")
  public Response createServices(String body, @Context HttpHeaders headers, @Context UriInfo ui) {

    return handleRequest(headers, body, ui, Request.Type.POST,
            createResource(null));
  }

  @PUT @Hidden // until documented
  @Path("{widgetLayoutId}")
  @Produces("text/plain")
  public Response updateService(String body, @Context HttpHeaders headers, @Context UriInfo ui,
                                @PathParam("widgetLayoutId") String widgetLayoutId) {

    return handleRequest(headers, body, ui, Request.Type.PUT, createResource(widgetLayoutId));
  }

  @PUT @Hidden // until documented
  @Produces("text/plain")
  public Response updateServices(String body, @Context HttpHeaders headers, @Context UriInfo ui) {

    return handleRequest(headers, body, ui, Request.Type.PUT, createResource(null));
  }

  @DELETE @Hidden // until documented
  @Path("{widgetLayoutId}")
  @Produces("text/plain")
  public Response deleteService(@Context HttpHeaders headers, @Context UriInfo ui,
                                @PathParam("widgetLayoutId") String widgetLayoutId) {

    return handleRequest(headers, null, ui, Request.Type.DELETE, createResource(widgetLayoutId));
  }

  private ResourceInstance createResource(String widgetLayoutId) {
    Map<Resource.Type,String> mapIds = new HashMap<>();
    mapIds.put(Resource.Type.WidgetLayout, widgetLayoutId);
    mapIds.put(Resource.Type.Cluster, clusterName);
    return createResource(Resource.Type.WidgetLayout, mapIds);
  }
}
