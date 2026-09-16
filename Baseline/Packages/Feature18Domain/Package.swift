// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature18Domain",
    products: [.library(name: "Feature18Domain", targets: ["Feature18Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature18Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
