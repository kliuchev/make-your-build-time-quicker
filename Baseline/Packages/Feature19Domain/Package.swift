// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature19Domain",
    products: [.library(name: "Feature19Domain", targets: ["Feature19Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature19Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
