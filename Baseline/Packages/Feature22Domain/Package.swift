// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature22Domain",
    products: [.library(name: "Feature22Domain", targets: ["Feature22Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature22Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
