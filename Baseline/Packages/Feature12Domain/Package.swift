// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature12Domain",
    products: [.library(name: "Feature12Domain", targets: ["Feature12Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature12Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
