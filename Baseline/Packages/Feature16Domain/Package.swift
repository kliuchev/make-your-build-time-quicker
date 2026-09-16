// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature16Domain",
    products: [.library(name: "Feature16Domain", targets: ["Feature16Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature16Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
