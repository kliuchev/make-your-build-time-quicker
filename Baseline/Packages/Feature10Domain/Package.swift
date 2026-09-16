// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature10Domain",
    products: [.library(name: "Feature10Domain", targets: ["Feature10Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature10Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
