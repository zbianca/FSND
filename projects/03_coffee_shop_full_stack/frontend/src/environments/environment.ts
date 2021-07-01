/*
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'coffee-shop-fs-bianca', // the auth0 domain prefix
    audience: 'https://coffee-shop-fs-bianca.eu.auth0.com', // the audience set for the auth0 app
    clientId: 'k2uaIHxIssazbkUThkr7B0ldpqsUmHFl', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application.
  }
};
