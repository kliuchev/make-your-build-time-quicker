// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature06Domain",
    products: [.library(name: "Feature06Domain", targets: ["Feature06Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature06Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
