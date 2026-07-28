---
section: Microservices
category: Architecture
tags: [concept]
---

# gRPC

## Definition

**gRPC** is a high-performance, language-agnostic RPC framework developed by Google. It uses Protocol Buffers (protobuf) for serialization and HTTP/2 for transport, enabling bidirectional streaming, flow control, and multiplexing. gRPC is widely adopted for microservice-to-microservice communication where performance matters.

## Why Do We Need It?

1. **Performance**: 5-10x faster than JSON/REST (binary protobuf serialization)
2. **HTTP/2**: Multiplexing, server push, bidirectional streaming, header compression
3. **Strong typing**: `.proto` files define service contracts in any language
4. **Code generation**: Client/server stubs auto-generated from `.proto` files
5. **Streaming**: Unary, server-streaming, client-streaming, bidirectional-streaming

## Code Examples

### Protobuf Definition

```protobuf
syntax = "proto3";

service UserService {
  rpc GetUser (GetUserRequest) returns (User);
  rpc ListUsers (ListUsersRequest) returns (stream User);
  rpc UpdateUser (stream UpdateUserRequest) returns (User);
  rpc Chat (stream ChatMessage) returns (stream ChatMessage);
}

message User {
  string id = 1;
  string name = 2;
  string email = 3;
}
```

### Node.js Server

```typescript
import * as grpc from '@grpc/grpc-js';
import { UserService } from './generated/user_grpc_pb';

const server = new grpc.Server();
server.addService(UserService, {
  getUser: (call, callback) => {
    const { id } = call.request;
    callback(null, { id, name: 'Alice', email: 'alice@example.com' });
  },
});
server.bindAsync('0.0.0.0:50051',
  grpc.ServerCredentials.createInsecure(), () => server.start());
```

## REST vs gRPC

| Feature | REST | gRPC |
|---------|:----:|:----:|
| Payload | JSON (human-readable) | Protobuf (binary) |
| Protocol | HTTP/1.1 | HTTP/2 |
| Streaming | ❌ | ✅ (bidirectional) |
| Code gen | Manual SDK | Auto-generated |
| Browser | Native | Requires gRPC-Web |

## Summary

- gRPC uses Protocol Buffers for efficient binary serialization and HTTP/2 for multiplexed streaming
- Four communication patterns: Unary, Server Streaming, Client Streaming, and Bidirectional Streaming
- Language-agnostic with auto-generated client/server stubs from .proto files
- Superior performance to REST/JSON for internal service-to-service communication
- Best suited for microservices, real-time streaming, and polyglot environments

---

### See Also

- [API Gateway](02-API-Gateway.md)
- [Interview Questions](08-Interview-Questions.md)
- [Kafka](05-Kafka.md)
- [REST APIs](../07-REST-API/)
- [Service Mesh](10-Service-Mesh.md)

## References & Learn More

- [gRPC Documentation](https://grpc.io/docs/)
- [gRPC Node.js](https://grpc.io/docs/languages/node/)
- [Protobuf Language Guide](https://protobuf.dev/programming-guides/proto3/)
