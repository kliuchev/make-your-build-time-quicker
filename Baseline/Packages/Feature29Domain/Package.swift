// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature29Domain",
    products: [.library(name: "Feature29Domain", targets: ["Feature29Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature29Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
