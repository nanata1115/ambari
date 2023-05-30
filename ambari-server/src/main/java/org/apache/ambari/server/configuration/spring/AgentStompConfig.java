/**
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
package org.apache.ambari.server.configuration.spring;

import com.google.inject.Injector;
import org.apache.ambari.server.agent.AgentSessionManager;
import org.apache.ambari.server.agent.stomp.HeartbeatController;
import org.apache.ambari.server.events.DefaultMessageEmitter;
import org.apache.ambari.server.events.listeners.requests.STOMPUpdateListener;
import org.apache.ambari.server.events.publishers.AmbariEventPublisher;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.messaging.simp.config.ChannelRegistration;
import org.springframework.messaging.simp.config.MessageBrokerRegistry;
import org.springframework.web.socket.config.annotation.*;
import org.springframework.web.socket.server.jetty.JettyRequestUpgradeStrategy;
import org.springframework.web.socket.server.support.DefaultHandshakeHandler;

@Configuration
@EnableWebSocket
@EnableWebSocketMessageBroker
@ComponentScan(basePackageClasses = {HeartbeatController.class})
@Import({RootStompConfig.class,GuiceBeansConfig.class})
public class AgentStompConfig implements WebSocketMessageBrokerConfigurer {
  private org.apache.ambari.server.configuration.Configuration configuration;

//  private final ServletContextHandler context;

  @Autowired
  private AgentRegisteringQueueChecker agentRegisteringQueueChecker;
  @Autowired
  private SimpMessagingTemplate brokerTemplate;

  public AgentStompConfig(Injector injector) {
//    this.context = context;
    configuration = injector.getInstance(org.apache.ambari.server.configuration.Configuration.class);
  }

  @Bean
  public DefaultMessageEmitter defaultMessageEmitter(Injector injector) {
    org.apache.ambari.server.configuration.Configuration configuration =
            injector.getInstance(org.apache.ambari.server.configuration.Configuration.class);
    return new DefaultMessageEmitter(injector.getInstance(AgentSessionManager.class),
            brokerTemplate,
            injector.getInstance(AmbariEventPublisher.class),
            configuration.getExecutionCommandsRetryCount(),
            configuration.getExecutionCommandsRetryInterval());
  }

  @Bean
  public STOMPUpdateListener requestSTOMPListener(Injector injector) {
    return new STOMPUpdateListener(injector, DefaultMessageEmitter.DEFAULT_AGENT_EVENT_TYPES);
  }

  public DefaultHandshakeHandler getHandshakeHandler() {
    DefaultHandshakeHandler defaultHandshakeHandler = new DefaultHandshakeHandler(new JettyRequestUpgradeStrategy());
    return defaultHandshakeHandler;
  }

  @Override
  public void registerStompEndpoints(StompEndpointRegistry registry) {
    registry.addEndpoint("/v1").setHandshakeHandler(getHandshakeHandler())
        .setAllowedOriginPatterns("*");

  }

  @Override
  public void configureClientInboundChannel(ChannelRegistration registration) {
    registration.taskExecutor().corePoolSize(configuration.getSpringMessagingThreadPoolSize());
  }

  @Override
  public void configureClientOutboundChannel(ChannelRegistration registration) {
    registration.taskExecutor().corePoolSize(configuration.getSpringMessagingThreadPoolSize());
    registration.interceptors(agentRegisteringQueueChecker);
  }

  @Override
  public void configureWebSocketTransport(WebSocketTransportRegistration registration) {
    registration.setMessageSizeLimit(configuration.getStompMaxIncomingMessageSize());
    registration.setSendBufferSizeLimit(configuration.getStompMaxBufferMessageSize());
  }

  @Override
  public void configureMessageBroker(MessageBrokerRegistry registry) {
    registry.setPreservePublishOrder(true);
  }
}
