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

import org.apache.ambari.server.security.AmbariEntryPoint;
import org.apache.ambari.server.security.authentication.AmbariDelegatingAuthenticationFilter;
import org.apache.ambari.server.security.authentication.AmbariLocalAuthenticationProvider;
import org.apache.ambari.server.security.authentication.jwt.AmbariJwtAuthenticationProvider;
import org.apache.ambari.server.security.authentication.kerberos.AmbariAuthToLocalUserDetailsService;
import org.apache.ambari.server.security.authentication.kerberos.AmbariKerberosAuthenticationProvider;
import org.apache.ambari.server.security.authentication.kerberos.AmbariKerberosTicketValidator;
import org.apache.ambari.server.security.authentication.kerberos.AmbariProxiedUserDetailsService;
import org.apache.ambari.server.security.authentication.pam.AmbariPamAuthenticationProvider;
import org.apache.ambari.server.security.authorization.AmbariAuthorizationFilter;
import org.apache.ambari.server.security.authorization.AmbariLdapAuthenticationProvider;
import org.apache.ambari.server.security.authorization.internal.AmbariInternalAuthenticationProvider;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.ProviderManager;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.access.intercept.FilterSecurityInterceptor;
import org.springframework.security.web.authentication.www.BasicAuthenticationFilter;

@Configuration
@EnableWebSecurity
@Import(GuiceBeansConfig.class)
@ComponentScan("org.apache.ambari.server.security")
public class ApiSecurityConfig {

  private final GuiceBeansConfig guiceBeansConfig;

  @Autowired
  private AmbariEntryPoint ambariEntryPoint;
  @Autowired
  private AmbariDelegatingAuthenticationFilter delegatingAuthenticationFilter;
  @Autowired
  private AmbariAuthorizationFilter authorizationFilter;

  public ApiSecurityConfig(GuiceBeansConfig guiceBeansConfig) {
    this.guiceBeansConfig = guiceBeansConfig;
  }

  @Autowired
  @Bean
  public AuthenticationManager authenticationManager(AmbariJwtAuthenticationProvider ambariJwtAuthenticationProvider,
                                                     AmbariPamAuthenticationProvider ambariPamAuthenticationProvider,
                                                     AmbariLocalAuthenticationProvider ambariLocalAuthenticationProvider,
                                                     AmbariLdapAuthenticationProvider ambariLdapAuthenticationProvider,
                                                     AmbariInternalAuthenticationProvider ambariInternalAuthenticationProvider,
                                                     AmbariKerberosAuthenticationProvider ambariKerberosAuthenticationProvider) throws Exception {
    return new ProviderManager(ambariJwtAuthenticationProvider,ambariPamAuthenticationProvider,
            ambariLocalAuthenticationProvider,ambariLdapAuthenticationProvider,
            ambariInternalAuthenticationProvider,ambariKerberosAuthenticationProvider);
  }

  @Bean
  public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http.csrf().disable().sessionManagement().sessionCreationPolicy(SessionCreationPolicy.IF_REQUIRED)
            .and()
            .authorizeHttpRequests().anyRequest().authenticated()
            .and()
            .headers().httpStrictTransportSecurity().disable()
            .frameOptions().disable().and()
            .exceptionHandling().authenticationEntryPoint(ambariEntryPoint)
            .and()
            .logout().logoutUrl("/api/v1/logout").deleteCookies("AMBARISESSIONID").clearAuthentication(true).invalidateHttpSession(true)
            .and()
            .addFilterBefore(guiceBeansConfig.ambariUserAuthorizationFilter(), BasicAuthenticationFilter.class)
            .addFilterAt(delegatingAuthenticationFilter, BasicAuthenticationFilter.class)
            .addFilterBefore(authorizationFilter, FilterSecurityInterceptor.class);
    return http.build();
  }

  @Bean
  public AmbariKerberosAuthenticationProvider ambariKerberosAuthenticationProvider(
      AmbariKerberosTicketValidator ambariKerberosTicketValidator,
      AmbariAuthToLocalUserDetailsService authToLocalUserDetailsService,
      AmbariProxiedUserDetailsService proxiedUserDetailsService) {

    return new AmbariKerberosAuthenticationProvider(authToLocalUserDetailsService,
        proxiedUserDetailsService,
        ambariKerberosTicketValidator);
  }
}
