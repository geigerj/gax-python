# Copyright 2015, Google Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Common utilities for Python code generated by Veneer Toolkit."""

from __future__ import absolute_import
from grpc.beta import implementations
from oauth2client import client as auth_client


def _oauth_access_token(scopes):
    google_creds = auth_client.GoogleCredentials.get_application_default()
    scoped_creds = google_creds.create_scoped(scopes)
    return scoped_creds.get_access_token().access_token


def create_stub(generated_create_stub, service_path, port, ssl_creds=None,
                channel=None, metadata_transformer=None, scopes=None):
    """Creates a gRPC client stub.

    Args:
        generated_create_stub: The generated gRPC method to create a stub.
        service_path: The DNS of the API remote host.
        port: The port on which to connect to the remote host.
        ssl_creds: A ClientCredentials object for use with an SSL-enabled
            Channel. If none, credentials are pulled from a default location.
        channel: A Channel object through which to make calls. If none, a secure
            channel is constructed.
        metadata_transformer: A function that transforms the metadata for
            requests, e.g., to give OAuth credentials.
        scopes: The OAuth scopes for this service. This parameter is ignored if
            a custom metadata_transformer is supplied.

    Returns:
        A gRPC client stub.
    """
    if scopes is None:
        scopes = []
    if channel is None:
        if ssl_creds is None:
            ssl_creds = implementations.ssl_client_credentials(None, None, None)
        else:
            ssl_creds = ssl_creds
        channel = implementations.secure_channel(service_path, port, ssl_creds)
    else:
        channel = channel

    if metadata_transformer is None:
        metadata_transformer = lambda x: [
            ('Authorization', 'Bearer %s' % _oauth_access_token(scopes))]
    else:
        metadata_transformer = metadata_transformer

    return generated_create_stub(channel,
                                 metadata_transformer=metadata_transformer)
