// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Shared",
    products: [.library(name: "Shared", targets: ["Shared"])],
    dependencies: [],
    targets: [.target(name: "Shared", dependencies: [])]
)
