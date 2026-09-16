// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature20Domain",
    products: [.library(name: "Feature20Domain", targets: ["Feature20Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature20Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
